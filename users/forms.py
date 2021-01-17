from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import User
from  django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email=forms.EmailField()
    first_name=forms.CharField(label='First Name')
    last_name=forms.CharField(label='last Name',required=False)
    class Meta:
        model=User
        fields =['username','email','first_name','last_name','password1','password2']

class UserUpdateForm(forms.ModelForm):
    email=forms.EmailField()
    first_name=forms.CharField(label='First Name')
    last_name=forms.CharField(label='last Name',required=False)
    
    class Meta:
        model=User
        fields =['username','email','first_name','last_name']

class ProfileUpdateForm(forms.ModelForm):
    bio=forms.CharField(label='bio',required= False)
    class Meta:
        model=Profile
        fields =['bio','image']

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name',required=False)
    email=forms.EmailField(required=True)
 
    def signup(self, request, User):
        User.first_name = self.cleaned_data['first_name']
        User.last_name = self.cleaned_data['last_name']
        User.email=self.cleaned_data['email']
        User.save()
        return user
