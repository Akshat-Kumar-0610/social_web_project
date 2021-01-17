from django import forms
from django.contrib.auth.models import User
from .models import post,Comment

class PostForm(forms.ModelForm):
    email=forms.EmailField()
    first_name=forms.CharField(label='First Name')
    last_name=forms.CharField(label='last Name',required=False)
    class Meta:
        model=post
        fields =['title','author','content','Date','image_post']

class CommentForm(forms.ModelForm):

    class Meta:
        model=Comment
        fields =['body']
