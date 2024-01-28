from user.models import User 

import httpx 

class TransferService: 
    @staticmethod
    def update_account_balance(data):        
        sent_user = User.objects.get(owner=data['sent_user'])
        received_user = User.objects.get(owner=data['received_user'])

        sent_user.account_balance -= data['value']
        received_user.account_balance += data['value']

        sent_user.save()
        received_user.save() 


class SimulateLoanService: 
    @staticmethod
    async def simulate_loan_api(request):
        url = 'http://127.0.0.1:3000/predict'
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
