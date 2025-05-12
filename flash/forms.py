from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, GameRating

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar', 'bio']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class GameRatingForm(forms.ModelForm):
    class Meta:
        model = GameRating
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '5',
                'step': '1'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '3',
                'placeholder': 'Оставьте свой комментарий...'
            })
        }
        labels = {
            'rating': 'Оценка (от 1 до 5)',
            'comment': 'Комментарий'
        } 