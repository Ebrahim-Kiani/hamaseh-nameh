from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, filters, permissions
from rest_framework.exceptions import PermissionDenied
from .models import memory, memory_pictures, memory_comments
from .seryalizers import memorySerializer, memory_picturesSerializer, memorylistSerializer, memory_commentsSerializer
from rest_framework.response import Response


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


# Reverse all memorys from a user(GET,DELETE,POST(post new object),PUT(update an object))
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
            raise PermissionDenied("You can only create memory_pictures for your own memorys.")


# Return filters of city or categories for user and Return search of memorys for user
class memoryListAPIView(generics.ListAPIView):
    serializer_class = memorylistSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['SubCategory__title', 'SubCategory__MainCategory__title', 'user__addresses__city']
    search_fields = [
        'title', 'user__full_name', 'SubCategory__title', 'SubCategory__MainCategory__title']
    queryset = memory.objects.all()

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


# Create comments on memorys
class memoryCommentsCreateAPIView(generics.CreateAPIView):
    serializer_class = memory_commentsSerializer
    queryset = memory_comments.objects.all()


class IsCommentOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the user is the owner of the comment
        return obj.user == request.user


# Edite comments on memorys
class memoryCommentsEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = memory_commentsSerializer
    queryset = memory_comments.objects.all()
    permission_classes = [IsCommentOwner]
