from django.db import models
from django.contrib.auth.models import User
class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")  
    cpf = models.CharField(max_length=14, unique=True, blank=True, null=True)  

    def __str__(self):
        return self.user.username
