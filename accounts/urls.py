from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/photo/delete/<int:photo_id>/', views.delete_gallery_photo, name='delete_gallery_photo'),
]
