from django.contrib.auth import get_user_model

# Create your tests here.

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken
User = get_user_model()
class UserLoginTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        # Create and save an active user in the test database
        cls.test_user_credentials = {
            'email': 'test@gmail.com',
            'password': '1234',
            'full_name':'tester'
        }
        cls.test_user = User.objects.create_user(**cls.test_user_credentials)
        cls.test_user.is_active = True
        cls.test_user.save()


def test_user_login(self):
    # Define the login URL
    login_url = reverse('token_obtain_pair')  # Replace with your JWT auth login URL

    # Credentials to be used for login
    login_credentials = {
        'email': self.test_user.email,
        'password': self.test_user_credentials['password']
    }

    # Perform a POST request to the login URL
    response = self.client.post(login_url, login_credentials, format='json')

    # Check if the login request was successful
    self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Check if both access and refresh tokens are returned in the response
    self.assertIn('access', response.data)
    self.assertIn('refresh', response.data)

    # Extract the tokens
    access_token = response.data['access']
    refresh_token = response.data['refresh']

    # Now we verify each token with the correct class
    try:
        # Verify the access token
        access_token_obj = AccessToken(access_token)
        self.assertTrue(access_token_obj.payload['user_id'] == self.test_user.id, 'Access token user_id does not match')

        # Verify the refresh token
        refresh_token_obj = RefreshToken(refresh_token)
        self.assertTrue(refresh_token_obj.payload['user_id'] == self.test_user.id,
                        'Refresh token user_id does not match')
    except TokenError as e:
        self.fail(f'Token validation has failed: {str(e)}')