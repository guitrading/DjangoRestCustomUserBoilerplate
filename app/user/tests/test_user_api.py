from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')        # Gets the url for the API create user endpoint
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')

def create_user(**params):
    """Create and returna new user"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the public features of the user API"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'john doe',
        }
        result = self.client.post(CREATE_USER_URL, payload)

        # Check if API endpoints returns successful creation status code
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email']) #Retrieves the e-mail address
        self.assertTrue(user.check_password(payload['password'])) #Check if the password matches the one for the user
        self.assertNotIn('password', result.data) #check if there is no password key in the response.

    def test_user_with_email_exists_error(self):
        """Test error returned if user with email already exists in the database"""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'john doe',
        }
        create_user(**payload)
        result = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test that password is too short error - less than 5 characters"""
        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'name': 'john doe',
        }
        response = self.client.post(CREATE_USER_URL, payload)
        user_exists = (get_user_model().objects.filter(
            email=payload['email'])
                       .exists())
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        user_details = {
            'name': 'john doe',
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        create_user(**user_details)
        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }
        response = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', response.data)       # Does it include the token
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        create_user(email="test@example.com", password="goodpass")
        payload = {
            'email': 'test@example.com',
            'password': 'badpass'
        }
        response = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Test if password is blank returns an error"""
        payload = {
            'email': 'test@example.com',
            'password': '',
        }
        response = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test that authentication is required for users"""
        response = self.client.get(ME_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test the private features of the user API that require authentication"""
    def setUp(self):
        self.user = create_user(
            email='test@example.com',
            password="testpass123",
            name='john doe',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)  # So for the remaining test
                                                        # we can assume user is authenticated

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user"""
        response = self.client.get(ME_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'email': self.user.email,
            'name': self.user.name,
        })

    def test_post_me_not_allowed(self):
        """Test that POST is not allowed for the me endpoint"""
        response = self.client.post(ME_URL, {})

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user"""
        payload = {'name': 'updated name', 'password': 'newpass123'}

        response = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)






