from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User

class RoomForm(forms.ModelForm):
  class Meta:
    model = Room
    fields = '__all__'
    exclude = ['host','participants']
    
class PostForm(forms.ModelForm):
  class Meta:
    model = Post
    fields = '__all__'
    exclude = ['author']
    
class CommentForm(forms.ModelForm):
  class Meta:
    model = Comment
    fields= '__all__'
    exclude = ['user','post']
    
class ProfileForm(forms.ModelForm):
  class Meta:
    model = Profile
    fields = '__all__'
    exclude = ['follows','user']
    
class UserUpdateForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ['username','first_name','last_name']