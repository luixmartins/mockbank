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
        url = 'http://127.0.0.1:8080/predict'
        data = []
        
        for input in request.POST: 
            try: 
                data.append(float(request.POST.get(input)))
            except: 
                pass 
        try: 
            async with httpx.AsyncClient() as client: 
                response = await client.post(url=url, json={'params': data})

                if response.status_code == 200: 
                    return response.json()
        
        except (httpx.HTTPError, httpx.RequestError) as error: 
            return f'Erro de solicitação: {error}'
