from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, filters, permissions, status
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .models import memory, memory_pictures, memory_comments, Rating, Bookmark
from .seryalizers import memorySerializer, memory_picturesSerializer, memorylistSerializer, memory_commentsSerializer, \
    RatingSerializer, BookmarkSerializer, TopTenUsersSerializers
from rest_framework.response import Response
from .models import Avg

from rest_framework.pagination import PageNumberPagination


class MemoryListPagination(PageNumberPagination):
    page_size = 10


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            try:
                if isinstance(view, memoryPicturesAPIView):
                    obj = memory_pictures.objects.get(pk=view.kwargs['pk'])
                    return obj.memory.user == request.user
                elif isinstance(view, memoryUserAPIView):
                    obj = memory.objects.get(pk=view.kwargs['pk'])
                    return obj.user == request.user
                else:
                    return False

            except (memory_pictures.DoesNotExist, memory.DoesNotExist):
                return False
        elif view.action == 'create':
            return True
        else:
            return view.action == 'list'
        return False


# Reverse all memories from a user(GET,DELETE,POST(post new object),PUT(update an object))
# Notice : pictures of a memory is readonly filed.
class memoryUserAPIView(viewsets.ModelViewSet):
    pagination_class = MemoryListPagination
    serializer_class = memorySerializer
    permission_classes = [IsOwnerOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        # Include the description field in the response
        data['description'] = instance.description

        return Response(data)

    def get_queryset(self):
        queryset = memory.objects.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class memoryPicturesAPIView(viewsets.ModelViewSet):
    serializer_class = memory_picturesSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = memory_pictures.objects.filter(memory__user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        memory = serializer.validated_data['memory']

        if memory.user == self.request.user:
            serializer.save()
        else:
            raise PermissionDenied("You can only create memory_pictures for your own memories.")


# Return filters of city or categories for user and Return search of memories for user
class memoryListAPIView(generics.ListAPIView):
    pagination_class = MemoryListPagination  # Ensure this is correctly defined
    serializer_class = memorylistSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['SubCategory__title', 'SubCategory__MainCategory__title', 'user__addresses__city', 'county']
    search_fields = [
        'title', 'user__full_name', 'SubCategory__title', 'SubCategory__MainCategory__title', 'county']
    queryset = memory.objects.all()

    def get_queryset(self):
        # Filter memories with status=True
        return memory.objects.filter(status=True)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Paginate the queryset
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = serializer.data

            # Remove unwanted fields
            for item in data:
                item.pop('pictures', None)
                item.pop('comments', None)

            # Use paginated response
            return self.get_paginated_response(data)

        # If no pagination, use default behavior
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        for item in data:
            item.pop('pictures', None)
            item.pop('comments', None)

        return Response(data)


# Retrieve memory details for user.
class memoryRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = memorylistSerializer
    queryset = memory.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        # Include the description field in the response
        data['description'] = instance.description

        return Response(data)


# Create comments on memories
class memoryCommentsCreateAPIView(generics.CreateAPIView):
    serializer_class = memory_commentsSerializer
    queryset = memory_comments.objects.all()


class IsCommentOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the user is the owner of the comment
        return obj.user == request.user


# Edite comments on memories
class memoryCommentsEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = memory_commentsSerializer
    queryset = memory_comments.objects.all()
    permission_classes = [IsCommentOwner]


class RatingCreateAPIView(generics.CreateAPIView):
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        memory_id = request.data.get('memory')
        value = request.data.get('value')

        # Check if the rating already exists
        rating, created = Rating.objects.update_or_create(
            memory_id=memory_id,
            user=user,
            defaults={'value': value}
        )

        if created:
            status_code = status.HTTP_201_CREATED  # New rating created
        else:
            status_code = status.HTTP_200_OK  # Existing rating updated

        # Call the UserPointsAPIView logic to recalculate and update the user's rating
        user_points_view = UserPointsAPIView()
        user = memory.objects.get(id=memory_id).user
        user_points_view.calculate_user_rating(user)

        serializer = self.get_serializer(rating)
        return Response(serializer.data, status=status_code)


class CountyListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        serializer_class = RatingSerializer
        permission_classes = [permissions.IsAuthenticated]
        counties = [
            "آران و بیدگل",
            "اردستان",
            "اصفهان",
            "برخوار",
            "بوئین و میاندشت",
            "تیران و کرون",
            "چادگان",
            "خمینی‌شهر",
            "خوانسار",
            "خور و بیابانک",
            "دهاقان",
            "سمیرم",
            "شاهین‌شهر و میمه",
            "شهرضا",
            "فریدن",
            "فریدون‌شهر",
            "فلاورجان",
            "کاشان",
            "گلپایگان",
            "لنجان",
            "مبارکه",
            "نایین",
            "نجف‌آباد",
            "نطنز"
        ]
        return Response(counties)


class BookmarkListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = BookmarkSerializer
    permission_classes = [IsAuthenticated]  # Ensure user is authenticated
    pagination_class = MemoryListPagination

    def list(self, request, *args, **kwargs):
        """Override list to include pagination."""
        queryset = self.filter_queryset(self.get_queryset())

        # Paginate the queryset
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # If no pagination, use default behavior
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):

        """Get all bookmarks for the logged-in user."""
        return Bookmark.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """Bookmark a memory."""
        memory_id = request.data.get('memory')  # Expect memory_id in the request body

        try:
            memory_instance = memory.objects.get(id=memory_id)  # Ensure the memory exists

            # Create or get the bookmark for the user
            bookmark, created = Bookmark.objects.get_or_create(user=request.user, memory=memory_instance)
            if created:
                return Response({"message": "خاطره مورد نظر با موفقیت ذخیره شد"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "خاطره مورد نظر از قبل ذخیره شده بود"}, status=status.HTTP_200_OK)
        except memory.DoesNotExist:
            return Response({"error": "خاطره مورد نظر پیدا نشد"}, status=status.HTTP_404_NOT_FOUND)


class BookMarkDestroyAPIView(generics.DestroyAPIView):
    BookmarkSerializer = BookmarkSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, pk=None):
        """Remove a bookmark"""
        try:
            bookmark = Bookmark.objects.get(memory=pk, user=request.user)
            bookmark.delete()
            return Response({"message": "خاطره مورد نظر با موفقیت حذف شد"}, status=status.HTTP_204_NO_CONTENT)
        except Bookmark.DoesNotExist:
            return Response({"error": "خاطره مورد نظر یافت نشد"}, status=status.HTTP_404_NOT_FOUND)


class TopRatedMemoriesAPIView(ListAPIView):
    serializer_class = memorylistSerializer

    def get_queryset(self):
        # Filter memories with status=True, order by rating descending, and limit to 10
        return memory.objects.filter(status=True).order_by('-average_rating')[:10]


User = get_user_model()


class UserPointsAPIView(APIView):
    def calculate_user_rating(self, user):
        """Helper method to calculate the total rating points for a user."""
        user_memories = memory.objects.filter(user=user)

        if not user_memories.exists():
            raise NotFound(detail="No memories found for the specified user.")

        # Calculate the sum of average_rating for all memories
        total_points = user_memories.aggregate(total_points=Sum('average_rating'))['total_points'] or 0.0

        # Update the user's rating
        user.Rating = total_points
        user.save()

        return total_points

    def get(self, request, *args, **kwargs):
        # Call the helper function to calculate the rating
        total_points = self.calculate_user_rating(request.user)

        return Response({"total_points": total_points})

class TopTenUserPointsAPIView(ListAPIView):
    serializer_class = TopTenUsersSerializers

    def get_queryset(self):
        # Filter memories with status=True, order by rating descending, and limit to 10
        return User.objects.filter(is_active=True).order_by('-Rating')[:10]