from django import forms
from .models import Patient, Doctor, Appointment, Treatment, Billing


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'
        widgets = {
            'patient_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'P001'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'registration_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'insurance_provider': forms.TextInput(attrs={'class': 'form-control'}),
            'insurance_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'
        widgets = {
            'doctor_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'D001'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'specialization': forms.Select(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'years_experience': forms.NumberInput(attrs={'class': 'form-control'}),
            'hospital_branch': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'
        widgets = {
            'appointment_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'A001'}),
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'appointment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'appointment_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'reason_for_visit': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class TreatmentForm(forms.ModelForm):
    class Meta:
        model = Treatment
        fields = '__all__'
        widgets = {
            'treatment_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'T001'}),
            'appointment': forms.Select(attrs={'class': 'form-control'}),
            'treatment_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'treatment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class BillingForm(forms.ModelForm):
    class Meta:
        model = Billing
        fields = '__all__'
        widgets = {
            'bill_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'B001'}),
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'treatment': forms.Select(attrs={'class': 'form-control'}),
            'bill_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'payment_status': forms.Select(attrs={'class': 'form-control'}),
        }
