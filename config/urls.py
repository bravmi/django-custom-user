from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/logout/', auth_views.LogoutView.as_view(next_page='/admin/')),
    path('admin/', admin.site.urls),
]
