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
            'farm_size': forms.NumberInput(attrs={'placeholder': 'Farm Size(Acres)', 'class': 'form-control form-control-lg'}),
        }
        
class CropForm(forms.ModelForm):
    class Meta:
        model = Crop
        fields = ['name', 'planting_date', 'growth_stage', 'next_activity', 'next_activity_date']

class ForumPostForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ['title', 'content']

class ForumCommentForm(forms.ModelForm):
    class Meta:
        model = ForumComment
        fields = ['content']

class CropListingForm(forms.ModelForm):
    class Meta:
        model = CropListing
        fields = ['crop', 'price', 'quantity']
