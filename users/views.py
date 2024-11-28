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
from .tasks import send_registration_email

def _create_user_and_profile(user_form, profile_form, request):
    try:
        user = user_form.save(commit=False)
        user.set_password(user_form.cleaned_data['password'])
        user.save()
        profile = profile_form.save(commit=False)
        profile.user = user
        profile.save()
        login(request, user)
        send_registration_email.delay(user.id)
        return JsonResponse({'redirect_url': '/'}, status=200)  # Redirect to home page
    except Exception as e:
        # Log the error
        print(f"Error creating user and profile: {e}")
        return JsonResponse({'errors': {'__all__': [str(e)]}}, status=500)

def _create_user_and_profile(user_form, profile_form, request):
    try:
        user = user_form.save(commit=False)
        user.set_password(user_form.cleaned_data['password'])
        user.save()
        profile = profile_form.save(commit=False)
        profile.user = user
        profile.save()
        login(request, user)
        send_registration_email(user)
        return JsonResponse({'redirect_url': '/'}, status=200)
    except Exception as e:
        print(f"Error creating user and profile: {e}")
        return JsonResponse({'errors': {'__all__': [str(e)]}}, status=500)

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

def send_registration_email(user):
    subject = 'Welcome to AgriSmart'
    message = f'Hi {user.username}, thank you for registering at AgriSmart.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject, message, email_from, recipient_list)

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
