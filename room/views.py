from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import RoomForm,PostForm,CommentForm,UserForm,ProfileForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

# Create your views here.


def loginPage(request):
  page = 'login'
  context = {'page':page}
  if request.user.is_authenticated:
    return redirect('home')
  if request.method == "POST":
    username = request.POST.get('username').lower()
    password = request.POST.get('password')
    try:
      user = User.objects.get(username=username)
    except:
      messages.error(request,'User does not exist!')
      
    user = authenticate(request,username=username,password=password)
    if user is not None:
      login(request,user)
      return redirect('home')
    else:
      messages.error(request,'Username or Password is wrong!')
  return render(request,'room/login_register.html',context)
  
  
def logoutUser(request):
  logout(request)
  return redirect('home')
  
  
def registerUser(request):
  form = UserCreationForm()
  if request.method == "POST":
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save(commit=False)
      user.username = user.username.lower()
      user.save()
      login(request,user)
      return redirect('home')
    else:
      messages.error(request,'An error occured during registration')
  context = {'form':form}
  return render(request,'room/login_register.html',context)
  
  
def home(request):
  q = request.GET.get('q') if request.GET.get('q') != None else ''
  rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q))
  room_count = rooms.count()
  topics = Topic.objects.all()
  room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))[0:5]
  context = {'rooms':rooms,'topics':topics,'room_count':room_count,'room_messages':room_messages}
  return render(request,'room/home.html',context)



@login_required(login_url='login')
def AllProfile(request):
  profiles = Profile.objects.exclude(user=request.user)
  context = {'profiles':profiles}
  return render(request,'room/profile_list.html',context)
  
  
def EachProfile(request,pk):
  profile = Profile.objects.get(id=pk)
  profile_form = ProfileForm()
  user_form = UserForm()
  if request.method == "POST":
    current_user_profile = request.user.profile
    data = request.POST
    action = data.get('follow')
    if action == "follow":
      current_user_profile.follows.add(profile)
    elif action == "unfollow":
      current_user_profile.follows.remove(profile)
    current_user_profile.save()    
  context = {'profile':profile,'profile_form':profile_form,'user_form':user_form}
  return render(request,'room/profile.html',context)
  
  
  
  
  
  
  
def room(request,pk):
  room = Room.objects.get(id=pk)
  room_messages = room.message_set.all().order_by('-created')
  participants = room.participants.all()
  if request.method == "POST":
    message = Message.objects.create(user = request.user,room = room,body = request.POST['body'])
    room.participants.add(request.user)
    return redirect('room',pk=room.id)
  context = {'room':room,'room_messages':room_messages,'participants':participants}
  return render(request,'room/room.html',context)
  

@login_required(login_url='login')
def CreateRoom(request):
  form = RoomForm()
  if request.method == "POST":
    form = RoomForm(request.POST)
    if form.is_valid():
      room = form.save(commit=False)
      room.host = request.user
      room.save()
      return redirect('home')
  context = {'form':form}
  return render(request,'room/room_form.html',context)
  
  
@login_required(login_url='login')  
def UpdateRoom(request,pk):
  room = Room.objects.get(id=pk)
  form = RoomForm(instance=room)
  if request.method == "POST":
    form = RoomForm(request.POST,instance=room)
    if form.is_valid():
      update = form.save(commit=False)
      update.user = request.user
      update.save()
      return redirect('home')
  context = {'form':form}
  return render(request,'room/room_form.html',context)
  


@login_required(login_url='login')
def DeleteRoom(request,pk):
  room = Room.objects.get(id=pk)
  if request.method == "POST":
    room.delete()
    return redirect('home')
  context = {'obj':room}
  return render(request,'room/delete.html',context)
  
  
@login_required(login_url='login')
def DeleteMessage(request,pk):
  message = Message.objects.get(id=pk)
  if request.method == "POST":
    message.delete()
    return redirect('home')
  context = {'obj':message}
  return render(request,'room/delete.html',context)



@login_required(login_url='login')
def post(request):
  posts = Post.objects.all()
  context = {'posts':posts}
  return render(request,'room/all_posts.html',context)
  
  
  
def PostDetail(request,pk):
  post = Post.objects.get(id=pk)
  comments = post.comments.all()
  comments_count = comments.count()
  comment_form = CommentForm()
  if request.method == "POST":
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
      comment = comment_form.save(commit=False)
      comment.user = request.user
      comment.post = post
      comment.save()
      return redirect('post-detail',post.id)
  context = {'post':post,'comments':comments,'comment_form':comment_form,'comments_count':comments_count}
  return render(request,'room/post_detail.html',context)
  
  
  
  
  
  
  
  
  
@login_required(login_url='login')  
def CreatePost(request):
  form = PostForm()
  if request.method == "POST":
    form = PostForm(request.POST,request.FILES)
    if form.is_valid():
      post = form.save(commit=False)
      post.author = request.user
      post.save()
      return redirect('post')
  context = {'form':form}
  return render(request,'room/create_post.html',context)
  
  
@login_required(login_url='login')  
def DeletePost(request,pk):
  post = Post.objects.get(id=pk)
  if request.method == "POST":
    post.delete()
    return redirect('post')
  context = {'obj':post}
  return render(request,'room/delete.html',context)
  
  
@login_required(login_url='login')  
def DeleteComment(request,pk):
  comment = Comment.objects.get(id=pk)
  if request.method == "POST":
    comment.delete()
    return redirect('post')
  context = {'obj':comment,'post':post}
  return render(request,'room/delete.html',context)  