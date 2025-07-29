from django.contrib import admin
from django.urls import path,include
from blog_app import views
urlpatterns = [
    path('',views.index,name="home"),
    path('singIn/',views.singIn,name="singIn"),
    path('logIn/',views.logIn,name="logIn"),
    path('logOut/',views.logOut,name="logOut"),
    path('show_post/',views.show_post,name="show_post"),
    path('add_post/',views.add_post,name="add_post"),
    path('my_post/',views.my_post,name="my_post"),
    path('edit/<int:post_id>/post',views.edit_post,name='edit_post'),
    path('search_post/',views.search_post,name="search_post"),
    path('delete/<int:post_id>/post',views.delete_post,name='delete_post'),

  
]