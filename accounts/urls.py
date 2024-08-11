from django.urls import path
from .views import (signup_view, login_view, logout_view, forgot_password_view, security_question_view, reset_password_view)

# URL patterns pro aplikaci accounts
urlpatterns = [
    path('signup/', signup_view, name='signup'),  # URL pro registraci uživatele
    path('login/', login_view, name='login'),  # URL pro přihlášení uživatele
    path('logout/', logout_view, name='logout'),  # URL pro odhlášení uživatele
    path('forgot_password/', forgot_password_view, name='forgot_password'),  # URL pro zapomenuté heslo
    path('security_question/', security_question_view, name='security_question'),  # URL pro bezpečnostní otázku
    path('reset_password/', reset_password_view, name='reset_password'),  # URL pro resetování hesla
]

