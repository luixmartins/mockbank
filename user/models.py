from django.db import models
from django.contrib.auth.models import User as DjangoUser 

import uuid 

class FinanceDataUser(models.Model):
    dependents = models.IntegerField(blank=True, default=0)
    education = models.IntegerField(default=0)
    employed = models.IntegerField(default=0)
    annual_income = models.DecimalField(max_digits=8, decimal_places=2, default=float(0), blank=True)
    score = models.IntegerField(default=500)
    residential_assets = models.DecimalField(max_digits=8, decimal_places=2, default=float(0), blank=True)
    commercial_assets = models.DecimalField(max_digits=8, decimal_places=2, default=float(0), blank=True)
    luxury_assets = models.DecimalField(max_digits=8, decimal_places=2, default=float(0), blank=True)
    bank_assets = models.DecimalField(max_digits=8, decimal_places=2, default=float(0), blank=True)
    active = models.BooleanField(default=False)
class User(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_phone = models.CharField(max_length=30, blank=True)

    account_balance = models.DecimalField(max_digits=8, decimal_places=2, default=float(0))
    account_limit = models.DecimalField(max_digits=8, decimal_places=2, default=float(0))

    owner = models.OneToOneField(DjangoUser, on_delete=models.CASCADE)
    finance_data = models.OneToOneField(FinanceDataUser, on_delete=models.CASCADE, null=True)

class UserMessages(models.Model): 
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    subject = models.CharField(max_length=100)
    message_content = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    response_from = models.OneToOneField('self', on_delete=models.CASCADE, null=True)
    
    message_from = models.ForeignKey(DjangoUser, on_delete=models.CASCADE, related_name='message_from')
    message_to = models.ForeignKey(DjangoUser, on_delete=models.CASCADE, related_name='message_to')
    
    message_read = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.subject  
    
    class Meta: 
        ordering = ["-created_at"]