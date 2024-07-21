from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import CustomUser

class UserAuthTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.forgot_password_url = reverse('forgot_password')
        self.security_question_url = reverse('security_question')
        self.reset_password_url = reverse('reset_password')

        # Create a test user
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpassword123',
            secret_question='What is your favorite book?',
            secret_answer='testanswer'
        )

    def test_signup(self):
        response = self.client.post(self.signup_url, {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
            'secret_question': 'What is your favorite color?',
            'secret_answer': 'blue'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after successful signup
        self.assertTrue(CustomUser.objects.filter(username='newuser').exists())

    def test_login(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword123'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after successful login
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_logout(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)  # Should redirect after logout
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_forgot_password(self):
        response = self.client.post(self.forgot_password_url, {
            'username': 'testuser'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect to security question page
        self.assertEqual(self.client.session['reset_user_id'], self.user.id)

    def test_security_question(self):
        self.client.post(self.forgot_password_url, {'username': 'testuser'})
        response = self.client.post(self.security_question_url, {
            'secret_answer': 'testanswer'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect to reset password page

    def test_reset_password(self):
        self.client.post(self.forgot_password_url, {'username': 'testuser'})
        self.client.post(self.security_question_url, {'secret_answer': 'testanswer'})
        response = self.client.post(self.reset_password_url, {
            'new_password1': 'newtestpassword123',
            'new_password2': 'newtestpassword123',
            'new_secret_question': 'What is your new favorite color?',
            'new_secret_answer': 'green'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after successful password reset
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newtestpassword123'))
        self.assertEqual(self.user.secret_question, 'What is your new favorite color?')
        self.assertEqual(self.user.secret_answer, 'green')
