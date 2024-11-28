from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register, weather_view, home_view, mpesa_payment_view, mpesa_callback_view, mpesa_payment_form_view, profile_view, profile_update_view
from .api_views import UserListCreateView, UserProfileListCreateView

urlpatterns = [
    path('register/', register, name='register'),
    path('weather/', weather_view, name='weather'),
    path('', home_view, name='home'),
    path('api/users/', UserListCreateView.as_view(), name='api_users'),
    path('api/userprofiles/', UserProfileListCreateView.as_view(), name='api_userprofiles'),
    path('mpesa/payment/', mpesa_payment_view, name='mpesa_payment'),
    path('mpesa/callback/', mpesa_callback_view, name='mpesa_callback'),
    path('mpesa/payment/form/', mpesa_payment_form_view, name='mpesa_payment_form'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', profile_update_view, name='profile_update'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]
