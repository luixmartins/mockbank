from django.urls import path 
from django.contrib.auth.decorators import login_required 

from user import views 

from user.views import HomePageView

app_name = 'user'

urlpatterns = [
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),  

    path("home/", HomePageView.as_view(), name="home"),

    path('user/create/', views.createUser, name='create'), 
    path('home/profile/', views.profileUser, name='profile'), 
]
