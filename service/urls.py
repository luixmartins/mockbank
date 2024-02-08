from django.urls import path 

from service import views 

app_name = 'service'

urlpatterns = [
    path('transfer/', views.TransferPage.as_view(), name='transfer'), 
    path('extract/', views.ExtractAccountView.as_view(), name='extract'), 
    path('loan-simulate/', views.NotLoggedLoan, name='loan_simulate'), 

    path('loan/', views.LoanSimulateView, name='loan'), 
]
