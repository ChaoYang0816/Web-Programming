from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('newUser/', views.newUser, name='newUser'),
    path('like/', views.like, name='like'),
    path('dislike/', views.dislike, name='dislike'),
    path('sortUserList/', views.sortUserList, name='sortUserList')
    #path('checkUser/', views.checkUser, name='checkUser')
]
