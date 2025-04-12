from django.core.management.base import BaseCommand
from Utilisateurs.models import Utilisateurs, User_role, RoleUserMapping

class Command(BaseCommand):
    help = 'Crée un utilisateur admin'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)
        parser.add_argument('--username', type=str, help='Username for admin')

    def handle(self, *args, **kwargs):
        email = kwargs['email']
        password = kwargs['password']
        # Utiliser l'email comme username par défaut si non fourni
        username = kwargs.get('username') or email.split('@')[0]

        try:
            # Créer l'utilisateur admin
            admin = Utilisateurs.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_staff=True,
                is_superuser=True
            )

            # Assigner le rôle admin
            admin_role = User_role.objects.get(roleName='admin')
            RoleUserMapping.objects.create(
                userID=admin,
                user_roleID=admin_role
            )

            self.stdout.write(self.style.SUCCESS(
                f'Admin créé avec succès: {email} (username: {username})'
            ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f'Erreur lors de la création de l\'admin: {str(e)}'
            ))