# users/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import UserRegistrationForm, UserProfileForm
from .weather_service import get_weather_data
from .mpesa_service import initiate_mpesa_payment
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.mail import send_mail
from django.conf import settings
from .email_utils import send_registration_email  # Import the new email utility function
import logging

logger = logging.getLogger(__name__)

def register(request):
    logger.info("Register view called")
    if request.method == 'POST':
        return _handle_post_request(request)
    user_form = UserRegistrationForm()
    profile_form = UserProfileForm()
    return render(request, 'users/register.html', {'user_form': user_form, 'profile_form': profile_form})

def _handle_post_request(request):
    user_form = UserRegistrationForm(request.POST)
    profile_form = UserProfileForm(request.POST)
    if user_form.is_valid() and profile_form.is_valid():
        logger.info("Forms are valid")
        return _create_user_and_profile(user_form, profile_form, request)
    logger.warning("Forms are not valid")
    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return render(request, 'users/register.html', {'user_form': user_form, 'profile_form': profile_form})
    errors = {**user_form.errors, **profile_form.errors}
    return JsonResponse({'errors': errors}, status=400)

def _create_user_and_profile(user_form, profile_form, request):
    try:
        logger.info("Creating user and profile")
        user = user_form.save(commit=False)
        user.set_password(user_form.cleaned_data['password'])
        user.save()
        profile = profile_form.save(commit=False)
        profile.user = user
        profile.save()
        login(request, user)
        logger.info("User and profile created, scheduling email")
        send_registration_email(user.email)  # Schedule the background task
        logger.info("Redirecting to home page")
        return redirect('home')
    except Exception as e:
        logger.error(f"Error creating user and profile: {e}")
        return render(request, 'users/register.html', {'user_form': user_form, 'profile_form': profile_form, 'errors': {'__all__': [str(e)]}})

def weather_view(request):
    if request.user.is_authenticated:
        profile = request.user.userprofile
        weather_data = get_weather_data(profile.farm_location)
        return render(request, 'users/weather.html', {'weather_data': weather_data})
    else:
        return redirect('login')

def home_view(request):
    return render(request, 'users/home.html')

def mpesa_payment_view(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        amount = request.POST.get('amount')
        response = initiate_mpesa_payment(phone_number, amount)
        return JsonResponse(response)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def mpesa_payment_form_view(request):
    return render(request, 'users/mpesa_payment.html')

@login_required
def profile_view(request):
    profile = request.user.userprofile
    return render(request, 'users/profile.html', {'profile': profile})

@login_required
def profile_update_view(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'users/profile_update.html', {'form': form})

@csrf_exempt
def mpesa_callback_view(request):
    if request.method == 'POST':
        mpesa_response = json.loads(request.body.decode('utf-8'))
        # Process the MPesa response here
        print(mpesa_response)  # For debugging purposes
        return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})
    return JsonResponse({"ResultCode": 1, "ResultDesc": "Invalid request"}, status=400)
