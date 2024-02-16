from django.db.models import Q 

from user.models import User 
from service.models import TransferModel, LoanModel

import httpx 
import datetime 

class TransferService: 
    @staticmethod
    def update_account_balance(data):        
        sent_user = User.objects.get(owner=data['sent_user'])
        received_user = User.objects.get(owner=data['received_user'])

        sent_user.account_balance -= data['value']
        received_user.account_balance += data['value']

        sent_user.save()
        received_user.save() 

    @staticmethod
    def verify_deposity_on_day(user) -> bool: 
        if TransferModel.objects.filter(sent_by=User.objects.get(owner=user), category='deposit').filter(created_at__date = datetime.date.today()):
            return False 
        return True 


class ExtractService: 
    @staticmethod
    def extract_account(filter_type, user_id): 
        if filter_type == "sent": 
            return TransferModel.objects.filter(sent_by=user_id, category='transfer')
        elif filter_type == "received": 
            return TransferModel.objects.filter(Q(received_by=user_id) | (Q(category='deposit') & Q(sent_by=user_id)))
        else: 
            return TransferModel.objects.filter(Q(sent_by=user_id) | Q(received_by=user_id))
            
class SimulateLoanService: 
    @staticmethod
    async def simulate_loan_api(request=None, data=None):
        url = 'http://127.0.0.1:3000/predict'

        if request: 
            data = {
                'dependentes': int(request.POST.get('dependents')), 
                'educacao': int(request.POST.get('education')), 
                'empregado': int(request.POST.get('employed')), 
                'renda_anual': float(request.POST.get('annual_income')), 
                'valor': float(request.POST.get('value')), 
                'pagamento': int(request.POST.get('payment')), 
                'score': int(request.POST.get('score')), 
                'patrimonio_residencial': float(request.POST.get('residential_assets')), 
                'patrimonio_comercial': float(request.POST.get('commercial_assets')), 
                'patrimonio_luxo': float(request.POST.get('luxury_assets')), 
                'patrimonio_bancario': float(request.POST.get('bank_assets')), 
            } 
        try: 
            async with httpx.AsyncClient() as client: 
                response = await client.post(url=url, json=data)

                if response.status_code == 200: 
                    response = response.json()
                    
                    return response['response']
                
                return None
        
        except (httpx.HTTPError, httpx.RequestError) as error: 
            return f'Erro de solicitação: {error}'

class GetFinanceDataService: 
    @staticmethod
    def get_finance_data(*args, **kwargs): 
        response = User.objects.get(owner=kwargs.get('user')) 
        
        return {
                'dependentes': int(response.finance_data.dependents), 
                'educacao': int(response.finance_data.education), 
                'empregado': int(response.finance_data.employed), 
                'renda_anual': float(response.finance_data.annual_income), 
                'valor': float(kwargs.get('value')), 
                'pagamento': int(kwargs.get('payment')), 
                'score': int(response.finance_data.score), 
                'patrimonio_residencial': float(response.finance_data.residential_assets), 
                'patrimonio_comercial': float(response.finance_data.commercial_assets), 
                'patrimonio_luxo': float(response.finance_data.luxury_assets), 
                'patrimonio_bancario': float(response.finance_data.bank_assets), 
            } 

class CreateNewLoanService: 
    @staticmethod
    def create_loan(**kwargs): 
        user = User.objects.get(owner=kwargs.get('user'))
        value = kwargs.get('value')
        payment = kwargs.get('payment')
        try: 
            queryset = LoanModel.objects.get(created_at__date = datetime.date.today())
            
            return False 
        except: 
            return LoanModel.objects.create(user=user, loan_value=value, payment=payment) 

