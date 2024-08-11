from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.forms import CustomUserCreationForm, CustomUserLoginForm, UsernameForm, SecurityQuestionForm, SetNewPasswordForm

User = get_user_model()

class AccountsTestCase(TestCase):
    """
    Testovací případ pro aplikaci accounts.
    """

    def setUp(self):
        """
        Nastavení testovacího prostředí před každým testem.
        Vytvoří uživatele a nastaví klienta.
        """
        self.user = User.objects.create_user(username='testuser', password='12345', secret_question='What is your favorite book?', secret_answer='TestAnswer')
        self.client = Client()

    def test_signup_view(self):
        """
        Testuje view pro registraci.
        Kontroluje, že uživatel může vytvořit nový účet a je přesměrován po úspěšné registraci.
        """
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'secret_question': 'What is your favorite color?',
            'secret_answer': 'Blue'
        })
        self.assertEqual(response.status_code, 302)  # Přesměrování po úspěšné registraci
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_view(self):
        """
        Testuje view pro přihlášení.
        Kontroluje, že uživatel může úspěšně přihlásit.
        """
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': '12345'
        })
        self.assertEqual(response.status_code, 302)  # Přesměrování po úspěšném přihlášení

    def test_logout_view(self):
        """
        Testuje view pro odhlášení.
        Kontroluje, že uživatel může úspěšně odhlásit.
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Přesměrování po úspěšném odhlášení

    def test_forgot_password_view(self):
        """
        Testuje view pro zapomenuté heslo.
        Kontroluje, že uživatel může zadat uživatelské jméno a přejít na bezpečnostní otázku.
        """
        response = self.client.post(reverse('forgot_password'), {
            'username': 'testuser'
        })
        self.assertEqual(response.status_code, 302)  # Přesměrování po úspěšném zadání uživatelského jména

    def test_security_question_view(self):
        """
        Testuje view pro bezpečnostní otázku.
        Kontroluje, že uživatel může zadat správnou odpověď a přejít na resetování hesla.
        """
        self.client.post(reverse('forgot_password'), {'username': 'testuser'})
        response = self.client.post(reverse('security_question'), {
            'secret_answer': 'TestAnswer'
        })
        self.assertEqual(response.status_code, 302)  # Přesměrování po správné odpovědi na bezpečnostní otázku

    def test_reset_password_view(self):
        """
        Testuje view pro resetování hesla.
        Kontroluje, že uživatel může úspěšně resetovat heslo.
        """
        self.client.post(reverse('forgot_password'), {'username': 'testuser'})
        self.client.post(reverse('security_question'), {'secret_answer': 'TestAnswer'})
        response = self.client.post(reverse('reset_password'), {
            'new_password1': 'newpassword',
            'new_password2': 'newpassword'
        })
        self.assertEqual(response.status_code, 302)  # Přesměrování po úspěšném resetování hesla
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword'))

    def test_invalid_secret_answer(self):
        """
        Testuje view pro bezpečnostní otázku s nesprávnou odpovědí.
        Kontroluje, že uživatel není přesměrován na resetování hesla po zadání nesprávné odpovědi.
        """
        self.client.post(reverse('forgot_password'), {'username': 'testuser'})
        response = self.client.post(reverse('security_question'), {
            'secret_answer': 'WrongAnswer'
        })
        self.assertEqual(response.status_code, 200)  # Zůstane na stránce bezpečnostní otázky
        self.assertContains(response, 'Incorrect answer to the secret question.')
