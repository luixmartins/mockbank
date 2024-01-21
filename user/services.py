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
        
        return {
            'balance': user.account_balance, 
            'limit': user.account_balance + user.account_limit, 
            'used_limit': user.account_limit - (user.account_balance + user.account_limit), 
        }

