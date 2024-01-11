from django.db import models
from django.contrib.auth.models import AbstractUser

import uuid 

class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_phone = models.CharField(max_length=20, blank=True)

    def __str__(self) -> str:
        return self.username 