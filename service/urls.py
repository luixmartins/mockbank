from django.urls import path 

from service import views 

app_name = 'service'

urlpatterns = [
    path('transfer/', views.TransferPage.as_view(), name='transfer'), 
]
