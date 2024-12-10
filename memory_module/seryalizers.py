from django.db.models import Avg
from rest_framework import serializers
from .models import memory, memory_pictures, memory_comments, Rating, Bookmark
from account_module.models import Address


class memory_commentsSerializer(serializers.ModelSerializer):
    user_full_name = serializers.SerializerMethodField()
    user_phone = serializers.SerializerMethodField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = memory_comments
        fields = '__all__'

    def get_user_full_name(self, obj):
        return obj.user.full_name

    def get_user_phone(self, obj):
        return obj.user.phone




class memory_picturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = memory_pictures
        fields = '__all__'


class memorySerializer(serializers.ModelSerializer):
    pictures = memory_picturesSerializer(many=True, read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    Sub_category_title = serializers.SerializerMethodField()
    main_picture_url = serializers.SerializerMethodField()
    comments = memory_commentsSerializer(many=True, read_only=True)

    class Meta:
        model = memory
        fields = ['id', 'title', 'SubCategory', 'Sub_category_title', 'user', 'main_picture', 'main_picture_url',
                  'pictures', 'description', 'comments', 'status', 'county']
        read_only_fields = ['status']  # Mark 'status' as read-only


    def update(self, instance, validated_data):
        validated_data.pop('description', None)
        return super().update(instance, validated_data)

    def get_main_picture_url(self, obj):
        if obj.main_picture and obj.main_picture.image:
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.main_picture.image.url)
        return None

    def get_Sub_category_title(self, obj):
        return obj.SubCategory.title

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.context['view'].action == 'retrieve':
            data['pictures'] = memory_picturesSerializer(instance.pictures.all(), many=True).data
            data['comments'] = memory_commentsSerializer(instance.comments.all(), many=True).data
        else:
            data.pop('pictures', None)
            data.pop('comments', None)
        return data


class memorylistSerializer(serializers.ModelSerializer):
    pictures = memory_picturesSerializer(many=True, read_only=True)
    comments = memory_commentsSerializer(many=True, read_only=True)
    user_full_name = serializers.SerializerMethodField()
    Sub_category_title = serializers.SerializerMethodField()
    user_phone = serializers.SerializerMethodField()
    user_avatar_url = serializers.SerializerMethodField()
    main_picture_url = serializers.SerializerMethodField()
    user_addresses_city = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()  # New field to check if bookmarked

    class Meta:
        model = memory
        fields = [
            'id', 'title', 'Sub_category_title', 'user_full_name', 'user_phone', 'user_addresses_city',
            'user_avatar_url', 'main_picture', 'main_picture_url', 'pictures', 'comments', 'average_rating','county'
            , 'is_bookmarked'
        ]
    def get_is_bookmarked(self, obj):
        # Check if the memory is bookmarked by the current user
        user = self.context['request'].user
        if not user.is_authenticated:
            return False  # If the user is not logged in, return False
        return Bookmark.objects.filter(user=user, memory=obj).exists()
    def get_user_full_name(self, obj):
        return obj.user.full_name

    # def get_rating(self, obj):
    #     # Calculate the average rating dynamically
    #     return obj.ratings.aggregate(avg_rating=Avg('value'))['avg_rating'] or 0.0


    def get_user_phone(self, obj):
        return obj.user.phone

    def get_main_picture_url(self, obj):
        if obj.main_picture and obj.main_picture.image:
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.main_picture.image.url)
        return None

    def get_user_avatar_url(self, obj):
        if obj.user.avatar:
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.user.avatar.url)
        return None

    def get_Sub_category_title(self, obj):
        return obj.SubCategory.title

    def get_user_addresses_city(self, obj):
        try:
            address = Address.objects.get(user=obj.user)
            return address.city
        except Address.DoesNotExist:
            return None


class RatingSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Rating
        fields = "__all__"

    def validate(self, attrs):
        user = self.context['request'].user
        memory = attrs.get('memory')

        if Rating.objects.filter(memory=memory, user=user).exists():
            raise serializers.ValidationError("You have already rated this memory.")

        return attrs

class BookmarkSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='memory.id', read_only=True)
    title = serializers.CharField(source='memory.title', read_only=True)
    Sub_category_title = serializers.CharField(source='memory.SubCategory.title', read_only=True)
    user_full_name = serializers.CharField(source='user.full_name', read_only=True)
    user_phone = serializers.CharField(source='memory.user.phone', read_only=True)
    user_addresses_city = serializers.CharField(source='memory.user.addresses.city', read_only=True)
    user_avatar_url = serializers.SerializerMethodField()
    main_picture = serializers.ImageField(source='memory.main_picture', read_only=True)
    main_picture_url = serializers.SerializerMethodField()
    average_rating = serializers.FloatField(source='memory.average_rating', read_only=True)

    class Meta:
        model = Bookmark
        fields = [
            'id', 'title', 'Sub_category_title', 'user_full_name',
            'user_phone', 'user_addresses_city', 'user_avatar_url',
            'main_picture', 'main_picture_url', 'average_rating'
        ]

    def get_user_avatar_url(self, obj):
        if obj.memory.user.avatar:
            return obj.memory.user.avatar.url
        return None

    def get_main_picture_url(self, obj):
        if obj.memory.main_picture and obj.memory.main_picture.image:
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.memory.main_picture.image.url)
        return None

from django.contrib.auth import get_user_model

User = get_user_model()
class TopTenUsersSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'full_name', 'Rating'
        ]

