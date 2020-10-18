from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.urls import path

urlpatterns = [
    path('admin/logout/', auth_views.LogoutView.as_view(next_page='/admin/')),
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('admin/')),
]
