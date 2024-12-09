from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, filters, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView

from .models import memory, memory_pictures, memory_comments, Rating
from .seryalizers import memorySerializer, memory_picturesSerializer, memorylistSerializer, memory_commentsSerializer, \
    RatingSerializer
from rest_framework.response import Response
from .models import Avg

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
    serializer_class = memorylistSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['SubCategory__title', 'SubCategory__MainCategory__title', 'user__addresses__city']
    search_fields = [
        'title', 'user__full_name', 'SubCategory__title', 'SubCategory__MainCategory__title']
    queryset = memory.objects.all()

    def get_queryset(self):
        # Filter memories with status=True
        return memory.objects.filter(status=True)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        for item in data:
            if 'pictures' in item:
                item.pop('pictures')
        for item in data:
            if 'comments' in item:
                item.pop('comments')

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

            serializer = self.get_serializer(rating)
            return Response(serializer.data, status=status_code)

    # def create(self, request, *args, **kwargs):
    #     data = request.data.copy()
    #     data['user'] = request.user.id  # Automatically set the user
    #
    #     serializer = self.get_serializer(data=data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #
    #     # After saving the rating, update the average rating for the memory
    #     memory = serializer.instance.memory
    #     memory.average_rating = memory.ratings.aggregate(Avg('value'))['value__avg']
    #     memory.save()
    #
    #
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

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