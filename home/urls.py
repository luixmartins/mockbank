from django.urls import path 

from home import views 

urlpatterns = [
    path('', views.home, name='home'), 
    path('contact-us/', views.contact_us, name='contact_us'), 
]
