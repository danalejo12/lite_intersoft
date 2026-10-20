
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Administrador
    path("admin/", admin.site.urls),

    # Inicio de sesión
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(
            template_name="accounts/login.html"
        ),
        name="login"
    ),

    # Cierre de sesión
    path(
        "accounts/logout/",
        auth_views.LogoutView.as_view(),
        name="logout"
    ),

    # Rutas de InterSoft Mini
    path("", include("core.urls")),
]
