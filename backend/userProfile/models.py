from django.db import models
from django.contrib.auth.models import User
# Create your models here.
import uuid

class Pasal(models.Model):
    user = models.ForeignKey(User, related_name='Pasals', on_delete=models.CASCADE)
    pasal_reference_name = models.CharField(max_length=200)
    pasal_address = models.CharField(max_length=100)
    pasal_uid = models.UUIDField(default=uuid.uuid4, editable=False,unique=True)
    password=models.CharField(max_length=30)
    # class Meta:
    #     unique_together=
    def __str__(self):
        return f'{self.user.username} {self.pasal_reference_name}'

class UserProfile(models.Model):
    user=models.OneToOneField(User,related_name='user_profile',on_delete=models.CASCADE)
  
    def __str__(self):
        return self.user.username
    
