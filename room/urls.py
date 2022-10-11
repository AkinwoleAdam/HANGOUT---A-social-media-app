from django.urls import path
from . import views

urlpatterns = [
  
  path('register/',views.registerUser,name='register'),
  
  path('login/',views.loginPage,name='login'),
  
  path('logout/',views.logoutUser,name='logout'),
  
  path('',views.home,name='home'),
  
  path('room/<str:pk>',views.room,name='room'),
  
  path('profile_list/',views.AllProfile,name='profile_list'),
  
  path('profile/<str:pk>',views.EachProfile,name='profile'),
  
  path('create-room/',views.CreateRoom,name='create-room'),
  
  path('update-room/<str:pk>',views.UpdateRoom,name='update-room'),
  
  path('delete-room/<str:pk>',views.DeleteRoom,name='delete-room'),
  
  path('delete-message/<str:pk>',views.DeleteMessage,name='delete-message'),
  
  path('all_posts/',views.post,name='post'),
  
  path('post_detail/<str:pk>',views.PostDetail,name='post-detail'),
  
  path('create-post/',views.CreatePost,name='create-post'),
  
  path('delete-post/<str:pk>',views.DeletePost,name='delete-post'),
  
  path('delete-comment/<str:pk>',views.DeleteComment,name='delete-comment'),
  ]