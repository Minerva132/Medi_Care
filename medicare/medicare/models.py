from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    patient_id = models.CharField(max_length=10, unique=True, primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    contact_number = models.CharField(max_length=15)
    address = models.TextField()
    registration_date = models.DateField()
    insurance_provider = models.CharField(max_length=100)
    insurance_number = models.CharField(max_length=50)
    email = models.EmailField()
    
    class Meta:
        ordering = ['patient_id']
    
    def __str__(self):
        return f"{self.patient_id} - {self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self):
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))


class Doctor(models.Model):
    SPECIALIZATIONS = [
        ('Cardiology', 'Cardiology'),
        ('Dermatology', 'Dermatology'),
        ('Pediatrics', 'Pediatrics'),
        ('Oncology', 'Oncology'),
        ('Neurology', 'Neurology'),
        ('Orthopedics', 'Orthopedics'),
        ('Other', 'Other'),
    ]
    
    doctor_id = models.CharField(max_length=10, unique=True, primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100, choices=SPECIALIZATIONS)
    phone_number = models.CharField(max_length=15)
    years_experience = models.IntegerField()
    hospital_branch = models.CharField(max_length=100)
    email = models.EmailField()
    
    class Meta:
        ordering = ['doctor_id']
    
    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name} - {self.specialization}"
    
    @property
    def full_name(self):
        return f"Dr. {self.first_name} {self.last_name}"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
        ('No-show', 'No-show'),
    ]
    
    REASON_CHOICES = [
        ('Checkup', 'Checkup'),
        ('Consultation', 'Consultation'),
        ('Follow-up', 'Follow-up'),
        ('Emergency', 'Emergency'),
        ('Therapy', 'Therapy'),
    ]
    
    appointment_id = models.CharField(max_length=10, unique=True, primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    reason_for_visit = models.CharField(max_length=100, choices=REASON_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Scheduled')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-appointment_date', '-appointment_time']
    
    def __str__(self):
        return f"{self.appointment_id} - {self.patient.full_name} with {self.doctor.full_name}"


class Treatment(models.Model):
    TREATMENT_TYPES = [
        ('X-Ray', 'X-Ray'),
        ('MRI', 'MRI'),
        ('ECG', 'ECG'),
        ('Chemotherapy', 'Chemotherapy'),
        ('Physiotherapy', 'Physiotherapy'),
        ('Surgery', 'Surgery'),
        ('Laboratory', 'Laboratory'),
    ]
    
    treatment_id = models.CharField(max_length=10, unique=True, primary_key=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='treatments')
    treatment_type = models.CharField(max_length=100, choices=TREATMENT_TYPES)
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    treatment_date = models.DateField()
    
    class Meta:
        ordering = ['-treatment_date']
    
    def __str__(self):
        return f"{self.treatment_id} - {self.treatment_type}"


class Billing(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('Cash', 'Cash'),
        ('Credit Card', 'Credit Card'),
        ('Debit Card', 'Debit Card'),
        ('Insurance', 'Insurance'),
        ('Online', 'Online'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Failed', 'Failed'),
        ('Refunded', 'Refunded'),
    ]
    
    bill_id = models.CharField(max_length=10, unique=True, primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='bills')
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE, related_name='bills')
    bill_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    
    class Meta:
        ordering = ['-bill_date']
    
    def __str__(self):
        return f"{self.bill_id} - ${self.amount} ({self.payment_status})"
