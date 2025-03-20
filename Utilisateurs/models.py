from django.db import models
from django.contrib.auth.models import AbstractUser

class Utilisateurs(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.username



class User_role(models.Model):
    ROLE_CHOICE = [
        ('admin', 'Administrateur'),
        ('enqueteur', 'Enquêteur'),
    ]

    roleName = models.CharField(max_length = 100, choices = ROLE_CHOICE, unique = True, default = 'enqueteur')
    description = models.TextField(blank = True, null = True) 

    def __str__(self):
        return self.roleName


class RoleUserMapping(models.Model):
    userID = models.ForeignKey(Utilisateurs, on_delete = models.CASCADE)
    user_roleID = models.ForeignKey(User_role, on_delete = models.CASCADE)

    def __str__(self):
        return f"{self.userID.email} - {self.user_roleID.roleName}"