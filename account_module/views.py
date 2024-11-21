from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Address, DiscountCode, Province, City
from .seryalizers import (UserSerialaizer, LoginSerializer, UserSettingSerializer, UserAddressSerializer
, ForgotPasswordLinkSerializer, DiscountCodeSerializer, UserDeleteAccountSerializer, ProvinceSerializer, CitySerializer)
from rest_framework import generics, status, views
from django.contrib.auth import get_user_model
from account_module.utils.jwt_token_generator import get_token_for_user
from .utils.generate_active_code import generate_activate_code
from validate_email_address import validate_email
from .utils.email_service import send_activation_email, expiretime_validator
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.

User = get_user_model()


class RegisterAPIView(generics.CreateAPIView):
    authentication_classes = []
    permission_classes = []

    queryset = User.objects.all()
    serializer_class = UserSerialaizer

    def perform_create(self, serializer, host, scheme):
        user = serializer.save()
        # Generate activation code and send email
        subject = 'Account Registration'
        template_name = 'email/activate_account.html'
        send_activation_email(user, template_name, subject, host, scheme)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')

        user = User.objects.filter(email=email).first()
        # Check if the email already exists in the database
        if user is not None:
            print(True)
            response_data = {
                'message': 'این ایمیل از قبل وارد شده است! لطفا یک ایمیل دیگر وارد کنید'
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        if not validate_email(email):
            print("email is not valid")
            response_data = {
                'message': 'ایمیل معتبر نیست یا از قبل ثبت شده است!! لطفا دوباره تلاش کنید'
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        host = request.META.get('HTTP_HOST')
        scheme = 'https' if request.is_secure() else 'http'

        self.perform_create(serializer, host, scheme)

        # Custom response
        response_data = {
            'message': 'کاربر با موفقیت ثبت نام شد.',
        }
        return Response(response_data, status=status.HTTP_201_CREATED)


class ActivateAccountAPIView(View):

    def get(self, request, active_code):
        user: User = User.objects.filter(email_active_code__iexact=active_code).first()
        if user is not None:
            if not expiretime_validator(user):
                if not user.is_active:
                    user.is_active = True
                    generate_activate_code(user)
                    message = {'message': 'Your account has been successfully activated'}
                    return JsonResponse(message
                                        , status=status.HTTP_201_CREATED)
                else:
                    message = {'message': 'Your account was active'}
                    return JsonResponse(message
                                        , status=status.HTTP_200_OK)
            else:
                message = {'message': 'Your active code is expired please resend it'}
                return JsonResponse(message
                                    , status=status.HTTP_400_BAD_REQUEST)

        else:
            message = {'message': 'Your account could not be found, the code may not be correct.'}
            return JsonResponse(message
                                , status=status.HTTP_404_NOT_FOUND)


class LoginAPIView(views.APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        host = request.META.get('HTTP_HOST')
        scheme = 'https' if request.is_secure() else 'http'
        context = {
            'host': host,
            'scheme': scheme
        }
        serializer = LoginSerializer(data=request.data, context=context)

        if serializer.is_valid():
            user = serializer.validated_data

            token = get_token_for_user(user)

            return Response(token, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class UserSettingAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSettingSerializer

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        original_email = user.email

        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Validate the email
        new_email = serializer.validated_data.get('email')
        if new_email and not validate_email(new_email):  # Assuming you have a validate_email function
            response_data = {
                'message': 'ایمیل معتبر نیست یا از قبل ثبت شده است! لطفا دوباره تلاش کنید'
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        # Get the image file from the request data
        image_file = request.data.get('avatar')

        # If the image file exists, modify the file name and save it
        if image_file:
            image_name = 'images/profile_images/' + image_file
            serializer.save(avatar=image_name)
        else:
            serializer.save()

        if new_email and original_email != new_email:
            user.email = new_email
            user.is_active = False  # Set user inactive until email is validated
            user.save()

            # Generate activation code and send email
            host = request.META.get('HTTP_HOST')
            scheme = 'https' if request.is_secure() else 'http'
            subject = 'Account Registration'
            template_name = 'email/activate_account.html'
            send_activation_email(user, template_name, subject, host, scheme)

            response_data = {
                'message': 'ایمیل شما با موفقیت ثبت شده است اما حساب کاربری شما فعال نیست!'
                           'لطفا صندوق ورودی خود را برای ایمیل تایید چک کنید',
                **serializer.data  # Unpack serializer data into the dictionary
            }
            return Response(response_data, status=status.HTTP_200_OK)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserAddressRetrieveAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserAddressSerializer

    def get_queryset(self):
        user = self.request.user
        return Address.objects.filter(user=user)

    def list(self, request, *args, **kwargs):
        user_addresses = self.get_queryset()
        serializer = self.get_serializer(user_addresses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        user = self.request.user
        province_name = request.data.get('province')
        city_name = request.data.get('city')

        try:
            province = Province.objects.get(name=province_name)
            city = City.objects.get(name=city_name)
        except (Province.DoesNotExist, City.DoesNotExist) as e:
            if isinstance(e, Province.DoesNotExist):
                message = 'Province does not exist.'
            else:
                message = 'City does not exist'
            return Response({'message': message}, status=status.HTTP_404_NOT_FOUND)

        try:
            address = Address.objects.create(user=user, province=province, city=city)
            serializer = UserAddressSerializer(address)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message': f'Error creating address: {e}'}, status=status.HTTP_400_BAD_REQUEST)


class UserAddressUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserAddressSerializer

    def get_object(self):
        user = self.request.user
        try:
            address_obj = Address.objects.get(pk=self.kwargs['pk'], user=user)
        except Address.DoesNotExist:
            return Response({'message': 'Address does not exist'}, status=status.HTTP_404_NOT_FOUND)

        return address_obj

    def retrieve(self, request, *args, **kwargs):
        user_addresses = self.get_object()
        serializer = self.get_serializer(user_addresses)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        user_address = self.get_object()

        try:
            user_address.province = Province.objects.get(name=request.data['province'])
        except:
            print('Province does not exist')

        try:
            user_address.city = City.objects.get(name=request.data['city'])
        except:
            print('City does not exist')

        user_address.save()

        serializer = self.get_serializer(user_address, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        user_address = self.get_object()

        try:
            user_address.delete()
        except:
            return Response({'message': 'Address does not exist'}, status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)


class ForgotPasswordAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        host = request.META.get('HTTP_HOST')
        scheme = 'https' if request.is_secure() else 'http'
        context = {
            'host': host,
            'scheme': scheme
        }
        serializer = ForgotPasswordLinkSerializer(data=request.data, context=context)  # Using the correct serializer

        if serializer.is_valid():
            serializer.save()  # This calls the save method on the serializer, where the email is sent

            # It's a good practice not to confirm whether an email exists in the database for security purposes.
            # You can return a generic message that doesn't indicate whether or not the email was found.
            return Response({
                'message': 'ما یک ایمیل برای تغیر رمز عبور برای شما ارسال کردیم'
            }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(View):
    authentication_classes = []
    permission_classes = []

    def get(self, request, active_code):

        return render(request, 'account_module/reset_password.html', {'active_code': active_code})

    def post(self, request, active_code):
        new_password = request.POST.get('new-password')

        try:
            # Retrieve the user object
            user = User.objects.get(email_active_code=active_code)

            # make hashing for set to data base and Set the new password

            user.set_password(new_password)
            user.save()

            # Optionally, log in the user automatically after password reset
            # auth.login(request, user)

            return HttpResponse("رمز با موفقیت تغیر کرد")
        except User.DoesNotExist:
            return HttpResponse("کاربر وجود ندارد")


class DiscountCodeAPIView(generics.RetrieveAPIView):
    serializer_class = DiscountCodeSerializer

    def get_object(self):
        user = self.request.user
        return DiscountCode.objects.get(code=self.kwargs['code'], user=user)

    def retrieve(self, request, *args, **kwargs):
        user_discount = self.get_object()
        serializer = self.get_serializer(user_discount)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            if not refresh_token:
                return Response({'error': 'Missing refresh token'}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({'message': 'شما با موفقیت خارج شدید!'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'یک خطا هنگام خروج پیش آمد لطفا دوباره تلاش کنید'}, status=status.HTTP_400_BAD_REQUEST)


class DeleteAccountView(APIView):
    serializer_class = UserDeleteAccountSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user.delete()
            return Response({'message': 'کاربر با موفقیت حذف شد'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProvinceListView(generics.ListAPIView):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer
    ordering = ['name']


class CityListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CitySerializer

    def post(self, request):
        try:
            province_name = request.data['province']
            if province_name:
                try:
                    province = Province.objects.get(name=province_name)
                    cities = City.objects.filter(province=province)
                except Province.DoesNotExist:
                    return Response({'error': 'Province not found'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'error': 'Province not found'}, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({'error': 'Province not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(cities, many=True)
        return Response(serializer.data)

    def get(self, request):
        cities = City.objects.all()
        serializer = self.serializer_class(cities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)