from user.models import User 

class TransferService: 
    @staticmethod
    def update_account_balance(data):        
        sent_user = User.objects.get(owner=data['sent_user'])
        received_user = User.objects.get(owner=data['received_user'])

        sent_user.account_balance -= data['value']
        received_user.account_balance += data['value']

        sent_user.save()
        received_user.save() 