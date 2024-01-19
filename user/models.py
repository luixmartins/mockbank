from django.db import models

# Create your models here.
from django.db import models 
from django.contrib.auth.models import User 

import uuid 

class User(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_phone = models.CharField(max_length=30, blank=True)

    account_balance = models.DecimalField(max_digits=8, decimal_places=2, default=float(0))
    account_limit = models.DecimalField(max_digits=8, decimal_places=2, default=float(0))

    owner = models.OneToOneField(User, on_delete=models.CASCADE)