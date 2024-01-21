from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User 

import uuid 
# Create your models here.
class TransferModel(models.Model):
    transfer_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    value = models.DecimalField(max_digits=8, decimal_places=2)
    
    sent_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_transfers')
    received_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_transfers')

    def __str__(self) -> str:
        return self.transfer_id
    
    class Meta: 
        ordering = ['-created_at']