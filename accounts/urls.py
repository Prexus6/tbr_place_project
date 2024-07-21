from django.urls import path
from .views import signup_view, login_view, logout_view, forgot_password_view, security_question_view, reset_password_view, index_view

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('forgot_password/', forgot_password_view, name='forgot_password'),
    path('security_question/', security_question_view, name='security_question'),
    path('reset_password/', reset_password_view, name='reset_password'),
    path('', index_view, name='index'),
]

