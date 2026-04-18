import csv
import os
from django.core.management.base import BaseCommand
from medicare.models import Patient, Doctor, Appointment, Treatment, Billing
from datetime import datetime


class Command(BaseCommand):
    help = 'Import data from CSV files into the database'

    def handle(self, *args, **kwargs):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        data_dir = os.path.join(base_dir, 'data')
        
        self.stdout.write(self.style.SUCCESS(f'Importing data from {data_dir}'))
        
        # Import Patients
        self.stdout.write('Importing patients...')
        patients_file = os.path.join(data_dir, 'patients.csv')
        with open(patients_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            patients_created = 0
            for row in reader:
                patient, created = Patient.objects.get_or_create(
                    patient_id=row['patient_id'],
                    defaults={
                        'first_name': row['first_name'],
                        'last_name': row['last_name'],
                        'gender': row['gender'],
                        'date_of_birth': datetime.strptime(row['date_of_birth'], '%Y-%m-%d').date(),
                        'contact_number': row['contact_number'],
                        'address': row['address'],
                        'registration_date': datetime.strptime(row['registration_date'], '%Y-%m-%d').date(),
                        'insurance_provider': row['insurance_provider'],
                        'insurance_number': row['insurance_number'],
                        'email': row['email'],
                    }
                )
                if created:
                    patients_created += 1
            self.stdout.write(self.style.SUCCESS(f'Successfully imported {patients_created} patients'))
        
        # Import Doctors
        self.stdout.write('Importing doctors...')
        doctors_file = os.path.join(data_dir, 'doctors.csv')
        with open(doctors_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            doctors_created = 0
            for row in reader:
                doctor, created = Doctor.objects.get_or_create(
                    doctor_id=row['doctor_id'],
                    defaults={
                        'first_name': row['first_name'],
                        'last_name': row['last_name'],
                        'specialization': row['specialization'],
                        'phone_number': row['phone_number'],
                        'years_experience': int(row['years_experience']),
                        'hospital_branch': row['hospital_branch'],
                        'email': row['email'],
                    }
                )
                if created:
                    doctors_created += 1
            self.stdout.write(self.style.SUCCESS(f'Successfully imported {doctors_created} doctors'))
        
        # Import Appointments
        self.stdout.write('Importing appointments...')
        appointments_file = os.path.join(data_dir, 'appointments.csv')
        with open(appointments_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            appointments_created = 0
            for row in reader:
                try:
                    patient = Patient.objects.get(patient_id=row['patient_id'])
                    doctor = Doctor.objects.get(doctor_id=row['doctor_id'])
                    appointment, created = Appointment.objects.get_or_create(
                        appointment_id=row['appointment_id'],
                        defaults={
                            'patient': patient,
                            'doctor': doctor,
                            'appointment_date': datetime.strptime(row['appointment_date'], '%Y-%m-%d').date(),
                            'appointment_time': datetime.strptime(row['appointment_time'], '%H:%M:%S').time(),
                            'reason_for_visit': row['reason_for_visit'],
                            'status': row['status'],
                        }
                    )
                    if created:
                        appointments_created += 1
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'Error importing appointment {row["appointment_id"]}: {e}'))
            self.stdout.write(self.style.SUCCESS(f'Successfully imported {appointments_created} appointments'))
        
        # Import Treatments
        self.stdout.write('Importing treatments...')
        treatments_file = os.path.join(data_dir, 'treatments.csv')
        with open(treatments_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            treatments_created = 0
            for row in reader:
                try:
                    appointment = Appointment.objects.get(appointment_id=row['appointment_id'])
                    treatment, created = Treatment.objects.get_or_create(
                        treatment_id=row['treatment_id'],
                        defaults={
                            'appointment': appointment,
                            'treatment_type': row['treatment_type'],
                            'description': row['description'],
                            'cost': float(row['cost']),
                            'treatment_date': datetime.strptime(row['treatment_date'], '%Y-%m-%d').date(),
                        }
                    )
                    if created:
                        treatments_created += 1
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'Error importing treatment {row["treatment_id"]}: {e}'))
            self.stdout.write(self.style.SUCCESS(f'Successfully imported {treatments_created} treatments'))
        
        # Import Billing
        self.stdout.write('Importing billing records...')
        billing_file = os.path.join(data_dir, 'billing.csv')
        with open(billing_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            billing_created = 0
            for row in reader:
                try:
                    patient = Patient.objects.get(patient_id=row['patient_id'])
                    treatment = Treatment.objects.get(treatment_id=row['treatment_id'])
                    bill, created = Billing.objects.get_or_create(
                        bill_id=row['bill_id'],
                        defaults={
                            'patient': patient,
                            'treatment': treatment,
                            'bill_date': datetime.strptime(row['bill_date'], '%Y-%m-%d').date(),
                            'amount': float(row['amount']),
                            'payment_method': row['payment_method'],
                            'payment_status': row['payment_status'],
                        }
                    )
                    if created:
                        billing_created += 1
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'Error importing bill {row["bill_id"]}: {e}'))
            self.stdout.write(self.style.SUCCESS(f'Successfully imported {billing_created} billing records'))
        
        self.stdout.write(self.style.SUCCESS('Data import completed successfully!'))
