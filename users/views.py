from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from .models import Crop, ForumPost, ForumComment, CropListing, TransactionRecord
from .forms import UserRegistrationForm, UserProfileForm, CropForm, ForumPostForm, ForumCommentForm, CropListingForm
from .weather_service import get_weather_data
from .mpesa_service import initiate_mpesa_payment
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.mail import send_mail
from django.conf import settings
from .email_utils import send_registration_email
from .analytics import predict_yield, provide_actionable_insights
import logging
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from .models import UserProfile

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
    user = None
    try:
        return _create_user_and_profile_logic(user_form, profile_form, request)
    except Exception as e:
        logger.error(f"Error creating user and profile: {e}")
        if user:
            user.delete()  # Clean up the user if profile creation fails
        return render(request, 'users/register.html', {'user_form': user_form, 'profile_form': profile_form, 'errors': {'__all__': [str(e)]}})

def _create_user_and_profile_logic(user_form, profile_form, request):
    logger.info("Creating user and profile")
    user = user_form.save(commit=False)
    user.is_active = False  # Deactivate account until it is confirmed
    user.set_password(user_form.cleaned_data['password'])
    user.save()
    logger.info(f"User created: {user.username}")

    profile = profile_form.save(commit=False)
    profile.user = user
    logger.info(f"Profile data: farm_location={profile.farm_location}, farm_size={profile.farm_size}")
    profile.save()
    logger.info(f"Profile created for user: {user.username}")

    current_site = get_current_site(request)
    mail_subject = 'Welcome to AgriSmart! Activate your account'
    message = render_to_string('registration/acc_active_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = user_form.cleaned_data.get('email')
    logger.info(f"Sending activation email to {to_email}")
    send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [to_email])
    logger.info("Activation email sent successfully")
    return render(request, 'registration/registration_complete.html')
    
@login_required
def profile_view(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    return render(request, 'users/profile.html', {'profile': profile})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is None or not default_token_generator.check_token(user, token):
        return render(request, 'registration/activation_invalid.html')
    
    user.is_active = True
    user.save()
    login(request, user)
    return redirect('home')

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

def home_view(request):
    featured_crops = Crop.objects.all()[:3]  # Get the first 3 crops
    recent_posts = ForumPost.objects.order_by('-created_at')[:5]  # Get the 5 most recent posts
    marketplace_listings = CropListing.objects.all()[:3]  # Get the first 3 listings

    print("Featured Crops:", featured_crops)
    print("Recent Posts:", recent_posts)
    print("Marketplace Listings:", marketplace_listings)

    context = {
        'featured_crops': featured_crops,
        'recent_posts': recent_posts,
        'marketplace_listings': marketplace_listings,
    }
    return render(request, 'users/home.html', context)

def about_view(request):
    return render(request, 'users/about.html')

def weather_view(request):
    if request.user.is_authenticated:
        profile = request.user.userprofile
        weather_data = get_weather_data(profile.farm_location)
        return render(request, 'users/weather.html', {'weather_data': weather_data})
    else:
        return redirect('login')

@csrf_exempt
@login_required
def mpesa_payment_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            phone_number = data.get('phone_number')
            amount = data.get('amount')
            listing_id = data.get('listing_id')
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        if not phone_number or not amount or not listing_id:
            logger.error("Missing required fields")
            return JsonResponse({'error': 'Phone number, amount, and listing ID are required'}, status=400)

        # Validate and format phone number
        if phone_number.startswith('0'):
            phone_number = f'254{phone_number[1:]}'
        elif phone_number.startswith('+'):
            phone_number = phone_number[1:]
        elif not phone_number.startswith('254'):
            logger.error("Invalid phone number format")
            return JsonResponse({'error': 'Invalid phone number format'}, status=400)

        # Validate amount
        try:
            amount = float(amount)
            if amount <= 0:
                logger.error("Amount must be a positive number")
                return JsonResponse({'error': 'Amount must be a positive number'}, status=400)
        except ValueError:
            logger.error("Invalid amount")
            return JsonResponse({'error': 'Invalid amount'}, status=400)

        # Initiate MPesa payment
        try:
            response = initiate_mpesa_payment(phone_number, amount)
            if 'error' not in response:
                # Store transaction record
                listing = get_object_or_404(CropListing, id=listing_id)
                TransactionRecord.objects.create(
                    user=request.user,
                    listing=listing,
                    phone_number=phone_number,
                    amount=amount,
                    transaction_id=response.get('CheckoutRequestID')
                )
            return JsonResponse(response)
        except Exception as e:
            logger.error(f"Error initiating MPesa payment: {e}")
            return JsonResponse({'error': 'Failed to initiate MPesa payment'}, status=500)
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

def is_manager_or_admin(user):
    return user.groups.filter(name__in=['Manager', 'Admin']).exists()

# @user_passes_test(is_manager_or_admin)
@login_required
def add_crop(request):
    logger.info(f"User {request.user.username} is attempting to add a crop")
    if request.method == 'POST':
        form = CropForm(request.POST)
        if form.is_valid():
            crop = form.save(commit=False)
            crop.user = request.user
            crop.save()
            logger.info(f"Crop {crop.name} added by user {request.user.username}")
            return redirect('crop_list')
        else:
            logger.warning(f"Form is not valid: {form.errors}")
    else:
        form = CropForm()
    return render(request, 'users/add_crop.html', {'form': form})

@login_required
def crop_list(request):
    crops = Crop.objects.filter(user=request.user)
    return render(request, 'users/crop_list.html', {'crops': crops})

@login_required
def crop_detail(request, crop_id):
    crop = get_object_or_404(Crop, id=crop_id)
    if crop.user != request.user:
        return redirect('home')
    yield_prediction = predict_yield(crop)
    insights = provide_actionable_insights(crop)
    return render(request, 'users/crop_detail.html', {'crop': crop, 'yield_prediction': yield_prediction, 'insights': insights})

@login_required
def edit_crop(request, crop_id):
    crop = get_object_or_404(Crop, id=crop_id, user=request.user)
    if request.method == 'POST':
        form = CropForm(request.POST, instance=crop)
        if form.is_valid():
            form.save()
            return redirect('crop_list')
    else:
        form = CropForm(instance=crop)
    return render(request, 'users/edit_crop.html', {'form': form})

@login_required
def delete_crop(request, crop_id):
    crop = get_object_or_404(Crop, id=crop_id, user=request.user)
    if request.method == 'POST':
        crop.delete()
        return redirect('crop_list')
    return render(request, 'users/delete_crop.html', {'crop': crop})

@login_required
def forum(request):
    posts = ForumPost.objects.all()
    return render(request, 'users/forum.html', {'posts': posts})

@login_required
def add_post(request):
    if request.method == 'POST':
        form = ForumPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('forum')
    else:
        form = ForumPostForm()
    return render(request, 'users/add_post.html', {'form': form})

def forum_post_detail(request, post_id):
    post = get_object_or_404(ForumPost, id=post_id)
    return render(request, 'users/forum_post_detail.html', {'post': post})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(ForumPost, id=post_id, user=request.user)
    if request.method == 'POST':
        form = ForumPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('forum')
    else:
        form = ForumPostForm(instance=post)
    return render(request, 'users/edit_post.html', {'form': form})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(ForumPost, id=post_id, user=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('forum')
    return render(request, 'users/delete_post.html', {'post': post})

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(ForumPost, id=post_id)
    if request.method == 'POST':
        form = ForumCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('forum')
    else:
        form = ForumCommentForm()
    return render(request, 'users/add_comment.html', {'form': form, 'post': post})

@login_required
def add_listing(request):
    if request.method == 'POST':
        form = CropListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user
            listing.save()
            return redirect('listing_list')
    else:
        form = CropListingForm()
    return render(request, 'users/add_listing.html', {'form': form})

@login_required
def listing_list(request):
    listings = CropListing.objects.all()
    return render(request, 'users/listing_list.html', {'listings': listings})

@login_required
def listing_detail(request, listing_id):
    listing = get_object_or_404(CropListing, id=listing_id)
    return render(request, 'users/listing_detail.html', {'listing': listing})

@login_required
def edit_listing(request, listing_id):
    listing = get_object_or_404(CropListing, id=listing_id, user=request.user)
    if request.method == 'POST':
        form = CropListingForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('listing_list')
    else:
        form = CropListingForm(instance=listing)
    return render(request, 'users/edit_listing.html', {'form': form})

@login_required
def delete_listing(request, listing_id):
    listing = get_object_or_404(CropListing, id=listing_id, user=request.user)
    if request.method == 'POST':
        listing.delete()
        return redirect('listing_list')
    return render(request, 'users/delete_listing.html', {'listing': listing})

@csrf_exempt
def mpesa_callback_view(request):
    logger.info("MPesa callback view called")
    logger.info(f"Request method: {request.method}")
    logger.info(f"Request headers: {request.headers}")
    logger.info(f"Request body: {request.body}")

    if request.method == 'POST':
        try:
            logger.info("Processing MPesa callback")
            mpesa_response = json.loads(request.body.decode('utf-8'))
            # Process the MPesa response here
            logger.info(f"MPesa response: {mpesa_response}")
            return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            return JsonResponse({"ResultCode": 1, "ResultDesc": "Invalid JSON format"}, status=400)
    elif request.method == 'GET':
        logger.warning("GET request received at MPesa callback URL")
        return JsonResponse({"ResultCode": 1, "ResultDesc": "This endpoint is for POST requests only"}, status=400)
    else:
        logger.warning("Invalid request method")
        return JsonResponse({"ResultCode": 1, "ResultDesc": "Invalid request"}, status=400)
