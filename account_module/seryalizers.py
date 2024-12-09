from abc import ABC

from django.contrib.auth.hashers import make_password

from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from .models import Address, DiscountCode, Province, City
from account_module.utils.email_service import send_activation_email

User = get_user_model()


class UserSerialaizer(serializers.ModelSerializer):

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data['password'] = make_password(password)
        return super().create(validated_data)

    class Meta:
        model = User
        fields = ['password', 'full_name', 'phone']


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        user = authenticate(phone=data.get('phone'), password=data.get('password'))

        if user is not None:
            if not user.is_active:
                host = self.context['host']
                scheme = self.context['scheme']
                subject = 'Account Registration'
                template_name = 'email/activate_account.html'
                send_activation_email(user, template_name, subject, host, scheme)
                raise serializers.ValidationError(
                    'Your account is not active. Please check your email for the confirmation link.'
                    'We sent new link for you.')
            else:
                return user
        raise serializers.ValidationError('شماره تلفن یا رمزعبور صحیح نیست!')

    class Meta:
        model = User
        fields = ['password', 'phone']


class UserSettingSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField('get_profile_image_url')

    def get_profile_image_url(self, obj):
        if obj.avatar:
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.avatar.url)
        return None

    class Meta:
        model = User
        fields = ['avatar', 'full_name', 'phone']


class UserAddressSerializer(serializers.ModelSerializer):
    province_name = serializers.SerializerMethodField()
    city_name = serializers.SerializerMethodField()

    def get_province_name(self, obj):
        try:
            if obj.province:
                return obj.province.name
            return None
        except:
            raise serializers.ValidationError('Not found!')

    def get_city_name(self, obj):
        try:
            if obj.city:
                return obj.city.name
            return None
        except:
            raise serializers.ValidationError('Not found!')

    class Meta:
        model = Address
        fields = ('id', 'user', 'province_name', 'city_name')


# class ForgotPasswordLinkSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(required=True)
#
#     def validate_email(self, value):
#         # Validation to check if the user with the given email exists
#         try:
#             user = User.objects.get(email=value)
#             self.context['user'] = user
#         except User.DoesNotExist:
#             raise serializers.ValidationError('A user with this email does not exist.')
#         return value
#
#     def save(self):
#         user = self.context['user']
#         host = self.context['host']
#         scheme = self.context['scheme']
#         subject = 'Account Forgot Password'
#         template_name = 'email/forgot_password.html'
#         # The `save` method is where you should invoke the email sending
#         send_activation_email(user, template_name, subject, host, scheme)
#         # You should not raise a ValidationError here unless there is an actual error.
#         return user
#
#     class Meta:
#         model = User
#         fields = ['email']


class DiscountCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCode
        fields = ['discount_percent', 'is_valid']


class UserDeleteAccountSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['password', 'phone']

    def validate(self, data):
        user = authenticate(phone=data.get('phone'), password=data.get('password'))

        if not user:
            raise serializers.ValidationError('Invalid credentials')
        else:
            return user


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'

class UserPublicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['avatar', 'full_name', 'phone']