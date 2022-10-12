from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import RoomForm,PostForm,CommentForm,ProfileForm,ProfileForm,UserUpdateForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

@login_required(login_url='account_login')
def home(request):
  posts = Post.objects.all()
  context = {'posts':posts}
  return render(request,'room/home.html',context)
  
@login_required(login_url='account_login')  
def CreatePost(request):
  form = PostForm()
  if request.method == "POST":
    form = PostForm(request.POST,request.FILES)
    if form.is_valid():
      post = form.save(commit=False)
      post.author = request.user
      post.save()
      return redirect('home')
  context = {'form':form}
  return render(request,'room/create_post.html',context)  
  
@login_required(login_url='account_login')
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
  
@login_required(login_url='account_login')  
def DeletePost(request,pk):
  post = Post.objects.get(id=pk)
  if request.method == "POST":
    post.delete()
    return redirect('home')
  context = {'obj':post}
  return render(request,'room/delete.html',context)
  
@login_required(login_url='account_login')  
def DeleteComment(request,pk):
  comment = Comment.objects.get(id=pk)
  if request.method == "POST":
    comment.delete()
    return redirect('post')
  context = {'obj':comment,'post':post}
  return render(request,'room/delete.html',context)    
  
@login_required(login_url='account_login')  
def allRooms(request):
  q = request.GET.get('q') if request.GET.get('q') != None else ''
  rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q))
  room_count = rooms.count()
  topics = Topic.objects.all()
  room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))[0:5]
  context = {'rooms':rooms,'topics':topics,'room_count':room_count,'room_messages':room_messages}
  return render(request,'room/all_rooms.html',context)

@login_required(login_url='account_login')
def CreateRoom(request):
  form = RoomForm()
  if request.method == "POST":
    form = RoomForm(request.POST)
    if form.is_valid():
      room = form.save(commit=False)
      room.host = request.user
      room.save()
      return redirect('all_rooms')
  context = {'form':form}
  return render(request,'room/room_form.html',context)

@login_required(login_url='account_login')  
def UpdateRoom(request,pk):
  room = Room.objects.get(id=pk)
  form = RoomForm(instance=room)
  if request.method == "POST":
    form = RoomForm(request.POST,instance=room)
    if form.is_valid():
      update = form.save(commit=False)
      update.user = request.user
      update.save()
      return redirect('all_rooms')
  context = {'form':form}
  return render(request,'room/room_form.html',context)

@login_required(login_url='account_login')
def DeleteRoom(request,pk):
  room = Room.objects.get(id=pk)
  if request.method == "POST":
    room.delete()
    return redirect('all_rooms')
  context = {'obj':room}
  return render(request,'room/delete.html',context)

@login_required(login_url='account_login')
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

@login_required(login_url='account_login')
def DeleteMessage(request,pk):
  message = Message.objects.get(id=pk)
  if request.method == "POST":
    message.delete()
    return redirect('all_rooms')
  context = {'obj':message}
  return render(request,'room/delete.html',context)

@login_required(login_url='account_login')
def Profiles(request):
  all_profiles = Profile.objects.exclude(user=request.user)
  context = {'all_profiles':all_profiles}
  return render(request,'room/profile_list.html',context)
  
@login_required(login_url='account_login')
def eachProfile(request,username):
  user = User.objects.get(username=username)
  profile = user.profile
  if request.method == "POST":
    current_user_profile = request.user.profile
    data = request.POST
    action = data.get('follow')
    if action == "follow":
      current_user_profile.follows.add(profile)
    elif action == "unfollow":
      current_user_profile.follows.remove(profile)
    current_user_profile.save()    
  context = {'profile':profile}
  return render(request,'room/profile.html',context)
  
@login_required(login_url='account_login')  
def editProfile(request,username):
  user = User.objects.get(username=username)
  profile = user.profile
  form = ProfileForm(instance=user.profile)
  user_form = UserUpdateForm(instance=user)
  if request.method == "POST":
    form = ProfileForm(request.POST,request.FILES,instance=user.profile)
    user_form = UserUpdateForm(request.POST,instance=user)
    if form.is_valid() and user_form.is_valid():
      form.save()
      user_form.save()
      messages.success(request,'Changes were made successfully!')
      return redirect('profile',profile.user.username)
  context = {'profile':profile,'form':form,'user_form':user_form}
  return render(request,'room/profile_edit.html',context)
  
def error_404(request, exception):
  return render(request, 'room/404.html')