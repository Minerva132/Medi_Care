from django.contrib import admin
from .models import Patient, Doctor, Appointment, Treatment, Billing


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['patient_id', 'full_name', 'gender', 'age', 'contact_number', 'insurance_provider']
    list_filter = ['gender', 'insurance_provider', 'registration_date']
    search_fields = ['patient_id', 'first_name', 'last_name', 'email', 'contact_number']
    date_hierarchy = 'registration_date'


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['doctor_id', 'full_name', 'specialization', 'hospital_branch', 'years_experience']
    list_filter = ['specialization', 'hospital_branch']
    search_fields = ['doctor_id', 'first_name', 'last_name', 'email']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['appointment_id', 'patient', 'doctor', 'appointment_date', 'appointment_time', 'status', 'reason_for_visit']
    list_filter = ['status', 'reason_for_visit', 'appointment_date']
    search_fields = ['appointment_id', 'patient__first_name', 'patient__last_name', 'doctor__first_name', 'doctor__last_name']
    date_hierarchy = 'appointment_date'
    raw_id_fields = ['patient', 'doctor']


@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    list_display = ['treatment_id', 'appointment', 'treatment_type', 'cost', 'treatment_date']
    list_filter = ['treatment_type', 'treatment_date']
    search_fields = ['treatment_id', 'appointment__patient__first_name', 'appointment__patient__last_name']
    date_hierarchy = 'treatment_date'
    raw_id_fields = ['appointment']


@admin.register(Billing)
class BillingAdmin(admin.ModelAdmin):
    list_display = ['bill_id', 'patient', 'amount', 'payment_status', 'payment_method', 'bill_date']
    list_filter = ['payment_status', 'payment_method', 'bill_date']
    search_fields = ['bill_id', 'patient__first_name', 'patient__last_name']
    date_hierarchy = 'bill_date'
    raw_id_fields = ['patient', 'treatment']
