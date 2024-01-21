from user.models import User as BaseUser 
from django.contrib.auth.models import User 

class UserService:
    @staticmethod
    def get_user_django(username: str):
        return User.objects.get(username=username)
    
    @staticmethod
    def get_user_app(pk: int):
        return BaseUser.objects.get(owner=pk)
    
    @staticmethod
    def user_balance(pk: int):
        user = UserService.get_user_app(pk)
        
        if user.account_balance >= 0:
            limit = user.account_limit
        else: 
            limit = user.account_balance + user.account_limit
            
        return {
            'balance': user.account_balance, 
            'limit': limit, 
            'used_limit': user.account_limit - (user.account_balance + user.account_limit), 
        }

