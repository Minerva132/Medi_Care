from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from medicare.models import Patient

class Command(BaseCommand):
    help = 'Create a test user (regular user, not admin)'

    def handle(self, *args, **kwargs):
        # Create regular user
        username = 'user'
        email = 'john.doe@email.com'
        password = 'user123'
        
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'User "{username}" already exists'))
            return
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name='John',
            last_name='Doe'
        )
        user.is_staff = False
        user.is_superuser = False
        user.save()
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created user: {username}'))
        self.stdout.write(self.style.SUCCESS(f'Password: {password}'))
        self.stdout.write(self.style.SUCCESS(f'Email: {email}'))
        
        # Link to existing patient record if available
        try:
            patient = Patient.objects.filter(email__iexact=email).first()
            if patient:
                self.stdout.write(self.style.SUCCESS(f'Linked to patient: {patient.full_name} ({patient.patient_id})'))
            else:
                self.stdout.write(self.style.WARNING('No patient record found with this email'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error linking patient: {str(e)}'))
