from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Crop, ForumPost, ForumComment, CropListing

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control form-control-lg'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control form-control-lg'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control form-control-lg'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control form-control-lg', 'type': 'email'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already in use.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['farm_location', 'farm_size']
        widgets = {
            'farm_location': forms.TextInput(attrs={'placeholder': 'Farm Location', 'class': 'form-control form-control-lg'}),
            'farm_size': forms.NumberInput(attrs={'placeholder': 'Farm Size (Acres)', 'class': 'form-control form-control-lg'}),
        }

class CustomDateInput(forms.DateInput):
    input_type = 'date'

    def __init__(self, attrs=None):
        if attrs is None:
            attrs = {}
        attrs['placeholder'] = attrs.get('placeholder', '')
        attrs['title'] = attrs.get('title', '')
        super().__init__(attrs)

GROWTH_STAGE_CHOICES = [
    ('', 'Select Growth Stage'),
    ('Seedling', 'Seedling'),
    ('Vegetative', 'Vegetative'),
    ('Flowering', 'Flowering'),
    ('Fruiting', 'Fruiting'),
    ('Mature', 'Mature'),
]

NEXT_ACTIVITY_CHOICES = [
    ('', 'Select Next Activity'),
    ('Watering', 'Watering'),
    ('Fertilizing', 'Fertilizing'),
    ('Weeding', 'Weeding'),
    ('Pest Control', 'Pest Control'),
    ('Harvesting', 'Harvesting'),
]

class CropForm(forms.ModelForm):
    class Meta:
        model = Crop
        fields = ['name', 'planting_date', 'growth_stage', 'next_activity', 'next_activity_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Crop Name'}),
            'planting_date': CustomDateInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Planting Date', 'title': 'Enter the date the crop was planted'}),
            'growth_stage': forms.Select(attrs={'class': 'form-control form-control-lg'}, choices=GROWTH_STAGE_CHOICES),
            'next_activity': forms.Select(attrs={'class': 'form-control form-control-lg'}, choices=NEXT_ACTIVITY_CHOICES),
            'next_activity_date': CustomDateInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Next Activity Date', 'title': 'Enter the date for the next activity'}),
        }

class ForumPostForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Title'}),
            'content': forms.Textarea(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Content'}),
        }

class ForumCommentForm(forms.ModelForm):
    class Meta:
        model = ForumComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Comment'}),
        }

class CropListingForm(forms.ModelForm):
    class Meta:
        model = CropListing
        fields = ['crop', 'price', 'quantity']
        widgets = {
            'crop': forms.Select(attrs={'class': 'form-control form-control-lg'}, choices=[('', 'Choose crop')] + [(crop.id, crop.name) for crop in Crop.objects.all()]),
            'price': forms.NumberInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Price', 'min': '0'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Quantity', 'min': '0'}),
        }
