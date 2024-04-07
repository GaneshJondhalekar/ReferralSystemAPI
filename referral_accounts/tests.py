from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import User

#Testcase for registration
class UserRegistrationTestCase(TestCase):
    def test_user_registration(self):
        client = APIClient()
        data = {
            'name': 'Ganesh',
            'email': 'gj@example.com',
            'password': 'password123'
        }
        response = client.post('/accounts/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('User_ID', response.data)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'registration successfull')

        # Ensure user is actually created in the database
        user = User.objects.get(email='gj@example.com')
        self.assertIsNotNone(user)

   
#Testcase for User details
class CurrentUserDetailsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='gj@example.com', password='password123', name='Test User')

    def test_user_details(self):
        # Authenticate user
        self.client.force_authenticate(user=self.user)

       
        response = self.client.get('/accounts/user_details/')
        
        # Check if response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if response contains user details
        self.assertEqual(response.data['message'], 'User details fetched successfully')
        self.assertEqual(response.data['status_code'], status.HTTP_200_OK)


class MyReferralsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_with_own_referral = User.objects.create_user(email='test1@example.com', password='password123', name='Test User 1')
        self.user_with_own_referral.own_referral_code = 'ABCDE'
        self.user_with_own_referral.save()

        self.user_with_referral = User.objects.create_user(email='test2@example.com', password='password123', name='Test User 2')
        self.user_with_referral.own_referral_code = 'FGHIJK'
        self.user_with_referral.referral_code = 'ABCDE'  # Use own_referral_code of first user
        self.user_with_referral.save()

   

    def test_my_referrals_with_referral(self):
        # Authenticate user with referral code
        self.client.force_authenticate(user=self.user_with_own_referral )

        
        response = self.client.get('/accounts/my_referrals/')
        print(response.data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

       
        self.assertEqual(response.data['results']['message'], 'My referrals fetched successfully')

    def test_my_referrals_with_no_referral(self):
        
        self.client.force_authenticate(user=self.user_with_referral)

        
        response = self.client.get('/accounts/my_referrals/')
        print(response.data)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

       
        self.assertEqual(response.data['message'], 'No referrals Found')
       

    