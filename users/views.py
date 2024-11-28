from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.http import JsonResponse
from .forms import UserRegistrationForm, UserProfileForm

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            return _create_user_and_profile(user_form, profile_form, request)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            errors = {**user_form.errors, **profile_form.errors}
            return JsonResponse({'errors': errors}, status=400)
    else:
        user_form = UserRegistrationForm()
        profile_form = UserProfileForm()
    
    return render(request, 'users/register.html', {'user_form': user_form, 'profile_form': profile_form})

def _create_user_and_profile(user_form, profile_form, request):
    try:
        user = user_form.save(commit=False)
        user.set_password(user_form.cleaned_data['password'])
        user.save()
        profile = profile_form.save(commit=False)
        profile.user = user
        profile.save()
        login(request, user)
        return JsonResponse({'redirect_url': '/'}, status=200)  # Redirect to home page
    except Exception as e:
        # Log the error
        print(f"Error creating user and profile: {e}")
        return JsonResponse({'errors': {'__all__': [str(e)]}}, status=500)
