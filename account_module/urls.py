from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [

    path('register/', views.RegisterAPIView.as_view(), name='register-url'),
    path('account/activator/<active_code>', views.ActivateAccountAPIView.as_view(), name='account-activator-url'),
    path('forgotpassword/', views.ForgotPasswordAPIView.as_view(), name='forgot-password-url'),
    path('resetpassword/<active_code>', views.ResetPasswordView.as_view(), name='account-reset-password'),
    path('login/', views.LoginAPIView.as_view(), name='login-url'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('logout/', views.LogoutAPIView.as_view(), name='logout'),
    path('delete-account/', views.DeleteAccountView.as_view(), name='delete-account-url'),
    path('settings/personal-info/', views.UserSettingAPIView.as_view(), name='user-personal-info-url'),
    path('settings/address-list/', views.UserAddressRetrieveAPIView.as_view(), name='user-address-list-url'),
    path('settings/address-edit/<int:pk>', views.UserAddressUpdateDestroyAPIView.as_view(), name='user-address-edit-url'),
    path('discountcode/validator/<code>', views.DiscountCodeAPIView.as_view(), name='discount-code-validator'),

    # Address
    path('provinces/', views.ProvinceListView.as_view(), name='province_list'),
    path('cities/', views.CityListView.as_view(), name='city_list'),

]