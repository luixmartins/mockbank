from django.urls import path 

from user import views 

app_name = 'user'

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.LogoutUser.as_view(), name='logout'),  

    path("home/", views.HomePageView.as_view(), name="home"),

    path('user/create/', views.CreateUser.as_view(), name='create'), 

    path('user/messages/', views.ListMessageUser.as_view(), name='list_messages'), 
    path('user/messages/new/', views.NewMessageView.as_view(), name='create_message'), 
    path('user/messages/<slug:message_id>/', views.MessageDetailView.as_view(), name='detail_message'),

    path('profile/', views.ProfileUser.as_view(), name='profile'), 
    
]
