from django.urls import path 

from user import views 

app_name = 'user'

urlpatterns = [
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),  
    path('home/', views.home, name='home'), 
    path('user/create/', views.createUser, name='create'), 
    path('home/profile/', views.profileUser, name='profile'), 
]
