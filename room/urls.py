from django.urls import path
from . import views

urlpatterns = [
  
  path('',views.home,name='home'),
  
  path('rooms/',views.allRooms,name='all_rooms'),
  
  path('room/<str:pk>',views.room,name='room'),
  
  path('profiles/',views.Profiles,name='profiles'),
  
  path('profile/<username>',views.eachProfile,name='profile'),
  
   path('profile/edit/<username>',views.editProfile,name='edit_profile'),
   
  path('create-room/',views.CreateRoom,name='create-room'),
  
  path('update-room/<str:pk>',views.UpdateRoom,name='update-room'),
  
  path('delete-room/<str:pk>',views.DeleteRoom,name='delete-room'),
  
  path('delete-message/<str:pk>',views.DeleteMessage,name='delete-message'),
  
  path('post_detail/<str:pk>',views.PostDetail,name='post-detail'),
  
  path('create-post/',views.CreatePost,name='create-post'),
  
  path('delete-post/<str:pk>',views.DeletePost,name='delete-post'),
  
  path('delete-comment/<str:pk>',views.DeleteComment,name='delete-comment'),
  ]
  
handler404 = 'room.views.error_404'