from django.db import models
from django.contrib.auth.models import User
from mimetypes import guess_type

# Create your models here.

class Topic(models.Model):
  name = models.CharField(max_length=200)
  def __str__(self):
    return self.name
    
class Room(models.Model):
  host = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
  topic = models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True)
  name = models.CharField(max_length=200)
  description = models.TextField(null=True,blank=True)
  participants = models.ManyToManyField(User,related_name='participants',blank=True)
  updated = models.DateTimeField(auto_now=True)
  created = models.DateTimeField(auto_now_add=True)
  class Meta:
    ordering = ['-updated','-created']
    
  def __str__(self):
    return self.name
    
class Message(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE)
  room = models.ForeignKey(Room,on_delete=models.CASCADE)
  body = models.TextField()
  updated = models.DateTimeField(auto_now=True)
  created = models.DateTimeField(auto_now_add=True)
  class Meta:
    ordering = ['-updated','-created']
  
  def __str__(self):
    return self.body[0:50]
    
class Post(models.Model):
  author = models.ForeignKey(User,related_name='author',on_delete=models.CASCADE,null=True)
  body = models.TextField(null=True)
  file = models.FileField(blank=True,null=True)
  created = models.DateTimeField(auto_now_add=True)
    
  def __str__(self):
    return self.body
    
  def get_type(self):
    file_type = guess_type(self.file.url, strict=True)[0]
    # file_type might be ('video/mp4', None) or ('image/jpeg..etc', None)
    if 'video' in file_type:
      return 'video'
    elif 'image' in file_type:
      return 'image'
  
  class Meta:
    ordering = ['-created']
    
class Comment(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
  post = models.ForeignKey(Post,related_name='comments',on_delete=models.SET_NULL,null=True)
  body = models.TextField(null=True)
  date_created = models.DateTimeField(auto_now_add=True)
  class Meta:
    ordering = ['-date_created']
    
  def __str__(self):
    return self.body
    
class Profile(models.Model):
  user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
  bio = models.TextField(null=True,blank=True)
  follows = models.ManyToManyField("self",related_name="followed_by",symmetrical=False,blank=True)
  website = models.URLField(null=True,blank=True)
  
  def __str__(self):
    return self.user.username