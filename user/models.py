from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class role(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return str(self.id)+'. '+str(self.name)
    
    class Meta:
        db_table = 'role'

class User(AbstractUser):
    role = models.ForeignKey(role, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    def __str__(self):
        return str(self.id)+'. '+str(self.username)
    
    class Meta:
        db_table = 'user'