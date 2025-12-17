"""
Management command to create a superuser for admin panel access.
This command creates a superuser with all necessary permissions.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()


class Command(BaseCommand):
    help = 'Create a superuser for admin panel access'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='Username for the superuser',
        )
        parser.add_argument(
            '--email',
            type=str,
            help='Email for the superuser',
        )
        parser.add_argument(
            '--password',
            type=str,
            help='Password for the superuser',
        )
        parser.add_argument(
            '--no-input',
            action='store_true',
            help='Run in non-interactive mode (requires --username, --email, --password)',
        )

    def handle(self, *args, **options):
        username = options.get('username')
        email = options.get('email')
        password = options.get('password')
        no_input = options.get('no_input', False)

        if no_input:
            if not username or not email or not password:
                self.stdout.write(
                    self.style.ERROR(
                        'Error: --no-input requires --username, --email, and --password'
                    )
                )
                return
        else:
            # Interactive mode
            if not username:
                username = input('Username: ')
            if not email:
                email = input('Email address: ')
            if not password:
                password = input('Password: ')
                password_confirm = input('Password (again): ')
                if password != password_confirm:
                    self.stdout.write(
                        self.style.ERROR('Error: Passwords do not match')
                    )
                    return

        # Validate input
        if not username:
            self.stdout.write(self.style.ERROR('Error: Username is required'))
            return
        if not email:
            self.stdout.write(self.style.ERROR('Error: Email is required'))
            return
        if not password:
            self.stdout.write(self.style.ERROR('Error: Password is required'))
            return

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'User "{username}" already exists.')
            )
            update = input('Do you want to update this user to superuser? (yes/no): ')
            if update.lower() in ['yes', 'y']:
                user = User.objects.get(username=username)
                user.is_superuser = True
                user.is_staff = True
                user.is_active = True
                if email:
                    user.email = email
                user.set_password(password)
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully updated user "{username}" to superuser.'
                    )
                )
                self._print_admin_info()
                return
            else:
                self.stdout.write(self.style.ERROR('Operation cancelled.'))
                return

        # Create superuser
        try:
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created superuser "{username}"'
                )
            )
            self._print_admin_info()
        except IntegrityError as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating superuser: {str(e)}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Unexpected error: {str(e)}')
            )

    def _print_admin_info(self):
        """Print admin panel access information"""
        from django.conf import settings
        admin_url = getattr(settings, 'ADMIN_URL', 'admin')
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('Admin Panel Access Information'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(f'Admin URL: http://127.0.0.1:8000/{admin_url}/')
        self.stdout.write('You can now access the admin panel using the credentials above.')
        self.stdout.write(self.style.SUCCESS('=' * 60))

