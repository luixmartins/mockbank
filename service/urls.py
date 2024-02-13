from django.urls import path 

from service import views 

app_name = 'service'

urlpatterns = [
    path('transfer/', views.TransferPage.as_view(), name='transfer'), 
    path('extract/', views.ExtractAccountView.as_view(), name='extract'), 
    path('loan-simulate/', views.NotLoggedLoan, name='loan_simulate'), 

    path('finance_data/contains/', views.FinanceDataUserView.as_view(), name='finance_data_content'),
    path('finance_data/update/', views.FinanceDataUserUpdateView.as_view(), name='finance_data_update'), 

    path('loan/', views.LoanView.as_view(), name='loan'),  
    path('verify_loan/', views.loan, name='verify_loan'), 
    path('confirm_loan/', views.ConfirmLoanView.as_view(), name='confirm_loan'), 

    path('deposit/', views.DepositView.as_view(), name='deposit'), 
]
