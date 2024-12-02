from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    register, weather_view, home_view, mpesa_payment_view, mpesa_callback_view, mpesa_payment_form_view,
    profile_view, profile_update_view, crop_list, add_crop, crop_detail, edit_crop, delete_crop,
    listing_list, add_listing, edit_listing, delete_listing, forum, add_post, add_comment
)
from .api_views import UserListCreateView, UserProfileListCreateView

urlpatterns = [
    path('', home_view, name='home'),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('weather/', weather_view, name='weather'),
    path('api/users/', UserListCreateView.as_view(), name='api_users'),
    path('api/userprofiles/', UserProfileListCreateView.as_view(), name='api_userprofiles'),
    path('mpesa/payment/', mpesa_payment_view, name='mpesa_payment'),
    path('mpesa/callback/', mpesa_callback_view, name='mpesa_callback'),
    path('mpesa/payment/form/', mpesa_payment_form_view, name='mpesa_payment_form'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', profile_update_view, name='profile_update'),
    path('crops/', crop_list, name='crop_list'),
    path('crops/add/', add_crop, name='add_crop'),
    path('crops/<int:crop_id>/', crop_detail, name='crop_detail'),
    path('crops/<int:crop_id>/edit/', edit_crop, name='edit_crop'),
    path('crops/<int:crop_id>/delete/', delete_crop, name='delete_crop'),
    path('marketplace/', listing_list, name='listing_list'),
    path('marketplace/add/', add_listing, name='add_listing'),
    path('marketplace/<int:listing_id>/edit/', edit_listing, name='edit_listing'),
    path('marketplace/<int:listing_id>/delete/', delete_listing, name='delete_listing'),
    path('forum/', forum, name='forum'),
    path('forum/add/', add_post, name='add_post'),
    path('forum/<int:post_id>/comment/', add_comment, name='add_comment'),
]
