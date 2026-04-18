from django.core.management.base import BaseCommand
from medicare.models import Patient

class Command(BaseCommand):
    help = 'Link test user to a patient record'

    def handle(self, *args, **kwargs):
        # Get first patient and update email
        patient = Patient.objects.first()
        
        if patient:
            old_email = patient.email
            patient.email = 'john.doe@email.com'
            patient.save()
            
            self.stdout.write(self.style.SUCCESS(f'Successfully linked patient {patient.patient_id} ({patient.full_name})'))
            self.stdout.write(self.style.SUCCESS(f'Updated email from {old_email} to {patient.email}'))
            self.stdout.write(self.style.SUCCESS(f'Test user "user" can now login and see this patient\'s data'))
        else:
            self.stdout.write(self.style.ERROR('No patients found in database'))
