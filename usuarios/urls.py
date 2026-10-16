from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'usuarios'

urlpatterns = [

    path("cadastro/", views.cadastro, name="cadastro"),
    path("login/", auth_views.LoginView.as_view(template_name="usuarios/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("password_reset/", auth_views.PasswordResetView.as_view(template_name="usuarios/password_reset.html"), name="password_reset"),
    path("perfil/", views.perfil, name="perfil"),
]