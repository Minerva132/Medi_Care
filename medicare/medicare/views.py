from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Sum, Q, Avg
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from .models import Patient, Doctor, Appointment, Treatment, Billing
from .forms import (
    PatientForm, DoctorForm, AppointmentForm, 
    TreatmentForm, BillingForm
)
from datetime import datetime, timedelta
import csv
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from .ai_diagnosis import SYMPTOMS, get_diagnosis, INSURANCE_COVERAGE


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'medicare/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully')
    return redirect('login')


@login_required
def dashboard(request):
    # Check if user is admin/staff
    if request.user.is_staff or request.user.is_superuser:
        return admin_dashboard(request)
    else:
        return user_dashboard(request)


@login_required
def admin_dashboard(request):
    # Statistics
    total_patients = Patient.objects.count()
    total_doctors = Doctor.objects.count()
    total_appointments = Appointment.objects.count()
    
    # Appointment statistics
    scheduled_appointments = Appointment.objects.filter(status='Scheduled').count()
    completed_appointments = Appointment.objects.filter(status='Completed').count()
    cancelled_appointments = Appointment.objects.filter(status='Cancelled').count()
    
    # Revenue statistics
    total_revenue = Billing.objects.aggregate(total=Sum('amount'))['total'] or 0
    paid_revenue = Billing.objects.filter(payment_status='Paid').aggregate(total=Sum('amount'))['total'] or 0
    pending_revenue = Billing.objects.filter(payment_status='Pending').aggregate(total=Sum('amount'))['total'] or 0
    
    # Recent appointments
    recent_appointments = Appointment.objects.select_related('patient', 'doctor').order_by('-appointment_date', '-appointment_time')[:5]
    
    # Upcoming appointments (today and future)
    today = datetime.now().date()
    upcoming_appointments = Appointment.objects.filter(
        appointment_date__gte=today,
        status='Scheduled'
    ).select_related('patient', 'doctor').order_by('appointment_date', 'appointment_time')[:5]
    
    # Appointment status distribution
    appointment_status_data = Appointment.objects.values('status').annotate(count=Count('status'))
    
    # Treatment type distribution
    treatment_type_data = Treatment.objects.values('treatment_type').annotate(count=Count('treatment_type')).order_by('-count')[:5]
    
    # Doctor specialization distribution
    specialization_data = Doctor.objects.values('specialization').annotate(count=Count('specialization'))
    
    context = {
        'total_patients': total_patients,
        'total_doctors': total_doctors,
        'total_appointments': total_appointments,
        'scheduled_appointments': scheduled_appointments,
        'completed_appointments': completed_appointments,
        'cancelled_appointments': cancelled_appointments,
        'total_revenue': total_revenue,
        'paid_revenue': paid_revenue,
        'pending_revenue': pending_revenue,
        'recent_appointments': recent_appointments,
        'upcoming_appointments': upcoming_appointments,
        'appointment_status_data': list(appointment_status_data),
        'treatment_type_data': list(treatment_type_data),
        'specialization_data': list(specialization_data),
    }
    
    return render(request, 'medicare/dashboard.html', context)


@login_required
def user_dashboard(request):
    """Dashboard for regular users (patients)"""
    # Get user's email to find their patient record
    user_email = request.user.email
    
    # Try to find patient by email or username
    try:
        patient = Patient.objects.filter(
            Q(email__iexact=user_email) | Q(first_name__icontains=request.user.username)
        ).first()
    except:
        patient = None
    
    # Get user's appointments
    if patient:
        my_appointments = Appointment.objects.filter(
            patient=patient
        ).select_related('doctor').order_by('-appointment_date', '-appointment_time')[:10]
        
        upcoming_appointments = Appointment.objects.filter(
            patient=patient,
            appointment_date__gte=datetime.now().date(),
            status='Scheduled'
        ).select_related('doctor').order_by('appointment_date', 'appointment_time')[:5]
        
        # Get assigned doctor (most recent appointment doctor)
        recent_appointment = Appointment.objects.filter(patient=patient).order_by('-appointment_date').first()
        assigned_doctor = recent_appointment.doctor if recent_appointment else None
        
        # Get billing status
        my_bills = Billing.objects.filter(patient=patient).order_by('-bill_date')[:5]
        total_bills = Billing.objects.filter(patient=patient).aggregate(total=Sum('amount'))['total'] or 0
        paid_bills = Billing.objects.filter(patient=patient, payment_status='Paid').aggregate(total=Sum('amount'))['total'] or 0
        pending_bills = total_bills - paid_bills
    else:
        my_appointments = []
        upcoming_appointments = []
        assigned_doctor = None
        my_bills = []
        total_bills = 0
        paid_bills = 0
        pending_bills = 0
    
    # Get available doctors for appointment booking
    available_doctors = Doctor.objects.all()
    
    context = {
        'patient': patient,
        'my_appointments': my_appointments,
        'upcoming_appointments': upcoming_appointments,
        'assigned_doctor': assigned_doctor,
        'my_bills': my_bills,
        'total_bills': total_bills,
        'paid_bills': paid_bills,
        'pending_bills': pending_bills,
        'available_doctors': available_doctors,
    }
    
    return render(request, 'medicare/user_dashboard.html', context)


# Patient Views
@login_required
def patient_list(request):
    search_query = request.GET.get('search', '')
    
    patients = Patient.objects.all()
    
    if search_query:
        patients = patients.filter(
            Q(patient_id__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(contact_number__icontains=search_query)
        )
    
    paginator = Paginator(patients, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    
    return render(request, 'medicare/patient_list.html', context)


@login_required
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    appointments = patient.appointments.all().order_by('-appointment_date')
    bills = patient.bills.all().order_by('-bill_date')
    
    context = {
        'patient': patient,
        'appointments': appointments,
        'bills': bills,
    }
    
    return render(request, 'medicare/patient_detail.html', context)


@login_required
def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Patient created successfully!')
            return redirect('patient_list')
    else:
        form = PatientForm()
    
    return render(request, 'medicare/patient_form.html', {'form': form, 'action': 'Create'})


@login_required
def patient_update(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, 'Patient updated successfully!')
            return redirect('patient_detail', pk=pk)
    else:
        form = PatientForm(instance=patient)
    
    return render(request, 'medicare/patient_form.html', {'form': form, 'action': 'Update', 'patient': patient})


@login_required
def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    
    if request.method == 'POST':
        patient.delete()
        messages.success(request, 'Patient deleted successfully!')
        return redirect('patient_list')
    
    return render(request, 'medicare/patient_confirm_delete.html', {'patient': patient})


# Doctor Views
@login_required
def doctor_list(request):
    search_query = request.GET.get('search', '')
    specialization = request.GET.get('specialization', '')
    
    doctors = Doctor.objects.all()
    
    if search_query:
        doctors = doctors.filter(
            Q(doctor_id__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    if specialization:
        doctors = doctors.filter(specialization=specialization)
    
    paginator = Paginator(doctors, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    specializations = Doctor.objects.values_list('specialization', flat=True).distinct()
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'specialization': specialization,
        'specializations': specializations,
    }
    
    return render(request, 'medicare/doctor_list.html', context)


@login_required
def doctor_detail(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    appointments = doctor.appointments.all().order_by('-appointment_date')
    
    context = {
        'doctor': doctor,
        'appointments': appointments,
    }
    
    return render(request, 'medicare/doctor_detail.html', context)


@login_required
def doctor_create(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Doctor created successfully!')
            return redirect('doctor_list')
    else:
        form = DoctorForm()
    
    return render(request, 'medicare/doctor_form.html', {'form': form, 'action': 'Create'})


@login_required
def doctor_update(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    
    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Doctor updated successfully!')
            return redirect('doctor_detail', pk=pk)
    else:
        form = DoctorForm(instance=doctor)
    
    return render(request, 'medicare/doctor_form.html', {'form': form, 'action': 'Update', 'doctor': doctor})


@login_required
def doctor_delete(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    
    if request.method == 'POST':
        doctor.delete()
        messages.success(request, 'Doctor deleted successfully!')
        return redirect('doctor_list')
    
    return render(request, 'medicare/doctor_confirm_delete.html', {'doctor': doctor})


# Appointment Views
@login_required
def appointment_list(request):
    search_query = request.GET.get('search', '')
    status = request.GET.get('status', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    
    appointments = Appointment.objects.select_related('patient', 'doctor').all()
    
    if search_query:
        appointments = appointments.filter(
            Q(appointment_id__icontains=search_query) |
            Q(patient__first_name__icontains=search_query) |
            Q(patient__last_name__icontains=search_query) |
            Q(doctor__first_name__icontains=search_query) |
            Q(doctor__last_name__icontains=search_query)
        )
    
    if status:
        appointments = appointments.filter(status=status)
    
    if date_from:
        appointments = appointments.filter(appointment_date__gte=date_from)
    
    if date_to:
        appointments = appointments.filter(appointment_date__lte=date_to)
    
    paginator = Paginator(appointments, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    statuses = Appointment.STATUS_CHOICES
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status': status,
        'date_from': date_from,
        'date_to': date_to,
        'statuses': statuses,
    }
    
    return render(request, 'medicare/appointment_list.html', context)


@login_required
def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment.objects.select_related('patient', 'doctor'), pk=pk)
    treatments = appointment.treatments.all()
    
    context = {
        'appointment': appointment,
        'treatments': treatments,
    }
    
    return render(request, 'medicare/appointment_detail.html', context)


@login_required
def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Appointment created successfully!')
            return redirect('appointment_list')
    else:
        form = AppointmentForm()
    
    return render(request, 'medicare/appointment_form.html', {'form': form, 'action': 'Create'})


@login_required
def appointment_update(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Appointment updated successfully!')
            return redirect('appointment_detail', pk=pk)
    else:
        form = AppointmentForm(instance=appointment)
    
    return render(request, 'medicare/appointment_form.html', {'form': form, 'action': 'Update', 'appointment': appointment})


@login_required
def appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    
    if request.method == 'POST':
        appointment.delete()
        messages.success(request, 'Appointment deleted successfully!')
        return redirect('appointment_list')
    
    return render(request, 'medicare/appointment_confirm_delete.html', {'appointment': appointment})


# Treatment Views
@login_required
def treatment_list(request):
    search_query = request.GET.get('search', '')
    treatment_type = request.GET.get('treatment_type', '')
    
    treatments = Treatment.objects.select_related('appointment__patient').all()
    
    if search_query:
        treatments = treatments.filter(
            Q(treatment_id__icontains=search_query) |
            Q(appointment__patient__first_name__icontains=search_query) |
            Q(appointment__patient__last_name__icontains=search_query)
        )
    
    if treatment_type:
        treatments = treatments.filter(treatment_type=treatment_type)
    
    paginator = Paginator(treatments, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    treatment_types = Treatment.TREATMENT_TYPES
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'treatment_type': treatment_type,
        'treatment_types': treatment_types,
    }
    
    return render(request, 'medicare/treatment_list.html', context)


@login_required
def treatment_detail(request, pk):
    treatment = get_object_or_404(Treatment.objects.select_related('appointment__patient', 'appointment__doctor'), pk=pk)
    bills = treatment.bills.all()
    
    context = {
        'treatment': treatment,
        'bills': bills,
    }
    
    return render(request, 'medicare/treatment_detail.html', context)


@login_required
def treatment_create(request):
    if request.method == 'POST':
        form = TreatmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Treatment created successfully!')
            return redirect('treatment_list')
    else:
        form = TreatmentForm()
    
    return render(request, 'medicare/treatment_form.html', {'form': form, 'action': 'Create'})


@login_required
def treatment_update(request, pk):
    treatment = get_object_or_404(Treatment, pk=pk)
    
    if request.method == 'POST':
        form = TreatmentForm(request.POST, instance=treatment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Treatment updated successfully!')
            return redirect('treatment_detail', pk=pk)
    else:
        form = TreatmentForm(instance=treatment)
    
    return render(request, 'medicare/treatment_form.html', {'form': form, 'action': 'Update', 'treatment': treatment})


@login_required
def treatment_delete(request, pk):
    treatment = get_object_or_404(Treatment, pk=pk)
    
    if request.method == 'POST':
        treatment.delete()
        messages.success(request, 'Treatment deleted successfully!')
        return redirect('treatment_list')
    
    return render(request, 'medicare/treatment_confirm_delete.html', {'treatment': treatment})


# Billing Views
@login_required
def billing_list(request):
    search_query = request.GET.get('search', '')
    payment_status = request.GET.get('payment_status', '')
    payment_method = request.GET.get('payment_method', '')
    
    bills = Billing.objects.select_related('patient', 'treatment').all()
    
    if search_query:
        bills = bills.filter(
            Q(bill_id__icontains=search_query) |
            Q(patient__first_name__icontains=search_query) |
            Q(patient__last_name__icontains=search_query)
        )
    
    if payment_status:
        bills = bills.filter(payment_status=payment_status)
    
    if payment_method:
        bills = bills.filter(payment_method=payment_method)
    
    paginator = Paginator(bills, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    payment_statuses = Billing.PAYMENT_STATUS_CHOICES
    payment_methods = Billing.PAYMENT_METHOD_CHOICES
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'payment_status': payment_status,
        'payment_method': payment_method,
        'payment_statuses': payment_statuses,
        'payment_methods': payment_methods,
    }
    
    return render(request, 'medicare/billing_list.html', context)


@login_required
def billing_detail(request, pk):
    bill = get_object_or_404(Billing.objects.select_related('patient', 'treatment'), pk=pk)
    
    context = {
        'bill': bill,
    }
    
    return render(request, 'medicare/billing_detail.html', context)


@login_required
def billing_create(request):
    if request.method == 'POST':
        form = BillingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bill created successfully!')
            return redirect('billing_list')
    else:
        form = BillingForm()
    
    return render(request, 'medicare/billing_form.html', {'form': form, 'action': 'Create'})


@login_required
def billing_update(request, pk):
    bill = get_object_or_404(Billing, pk=pk)
    
    if request.method == 'POST':
        form = BillingForm(request.POST, instance=bill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bill updated successfully!')
            return redirect('billing_detail', pk=pk)
    else:
        form = BillingForm(instance=bill)
    
    return render(request, 'medicare/billing_form.html', {'form': form, 'action': 'Update', 'bill': bill})


@login_required
def billing_delete(request, pk):
    bill = get_object_or_404(Billing, pk=pk)
    
    if request.method == 'POST':
        bill.delete()
        messages.success(request, 'Bill deleted successfully!')
        return redirect('billing_list')
    
    return render(request, 'medicare/billing_confirm_delete.html', {'bill': bill})


# Export Views
@login_required
def export_patients_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="patients.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Patient ID', 'Name', 'Gender', 'Date of Birth', 'Contact', 'Email', 'Insurance Provider', 'Insurance Number'])
    
    patients = Patient.objects.all()
    for patient in patients:
        writer.writerow([
            patient.patient_id,
            patient.full_name,
            patient.get_gender_display(),
            patient.date_of_birth,
            patient.contact_number,
            patient.email,
            patient.insurance_provider,
            patient.insurance_number
        ])
    
    return response


@login_required
def export_billing_pdf(request, pk):
    bill = get_object_or_404(Billing.objects.select_related('patient', 'treatment'), pk=pk)
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    title = Paragraph(f"<b>INVOICE - {bill.bill_id}</b>", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 0.3*inch))
    
    # Patient Information
    patient_info = Paragraph(f"""
        <b>Patient Information:</b><br/>
        Name: {bill.patient.full_name}<br/>
        Patient ID: {bill.patient.patient_id}<br/>
        Email: {bill.patient.email}<br/>
        Contact: {bill.patient.contact_number}
    """, styles['Normal'])
    elements.append(patient_info)
    elements.append(Spacer(1, 0.3*inch))
    
    # Treatment Information
    treatment_info = Paragraph(f"""
        <b>Treatment Information:</b><br/>
        Treatment Type: {bill.treatment.treatment_type}<br/>
        Description: {bill.treatment.description}<br/>
        Treatment Date: {bill.treatment.treatment_date}
    """, styles['Normal'])
    elements.append(treatment_info)
    elements.append(Spacer(1, 0.3*inch))
    
    # Billing Information
    data = [
        ['Description', 'Amount'],
        ['Treatment Cost', f'${bill.amount}'],
        ['Payment Method', bill.payment_method],
        ['Payment Status', bill.payment_status],
        ['Bill Date', str(bill.bill_date)],
    ]
    
    table = Table(data, colWidths=[3*inch, 2*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    
    doc.build(elements)
    
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{bill.bill_id}.pdf"'
    
    return response


# AI Diagnosis Views
@login_required
def ai_diagnosis_view(request):
    """AI-powered diagnosis page"""
    context = {
        'symptoms': SYMPTOMS,
        'insurance_types': list(INSURANCE_COVERAGE.keys()),
    }
    return render(request, 'medicare/ai_diagnosis.html', context)


@login_required
def ai_diagnosis_result(request):
    """Process diagnosis and show results"""
    if request.method == 'POST':
        # Get form data
        full_name = request.POST.get('full_name')
        age = int(request.POST.get('age', 0))
        gender = request.POST.get('gender')
        contact = request.POST.get('contact')
        insurance = request.POST.get('insurance')
        symptoms = request.POST.getlist('symptoms')
        
        # Validate
        if not all([full_name, age, gender, contact]) or len(symptoms) == 0:
            messages.error(request, 'Please fill all required fields and select at least one symptom.')
            return redirect('ai_diagnosis')
        
        if len(symptoms) > 15:
            messages.error(request, 'Please select maximum 15 symptoms.')
            return redirect('ai_diagnosis')
        
        # Get diagnosis
        result = get_diagnosis(full_name, age, gender, contact, insurance, symptoms)
        
        if not result:
            messages.error(request, 'Unable to generate diagnosis. Please try again.')
            return redirect('ai_diagnosis')
        
        return render(request, 'medicare/ai_diagnosis_result.html', {'result': result})
    
    return redirect('ai_diagnosis')


# User Appointment Booking
@login_required
def user_book_appointment(request):
    """Allow users to book appointments"""
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        doctor_id = request.POST.get('doctor_id')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        reason = request.POST.get('reason', '')
        
        try:
            patient = Patient.objects.get(patient_id=patient_id)
            doctor = Doctor.objects.get(doctor_id=doctor_id)
            
            # Generate appointment ID
            last_appointment = Appointment.objects.order_by('-appointment_id').first()
            if last_appointment:
                last_num = int(last_appointment.appointment_id[1:])
                new_id = f'A{str(last_num + 1).zfill(3)}'
            else:
                new_id = 'A001'
            
            # Create appointment
            appointment = Appointment.objects.create(
                appointment_id=new_id,
                patient=patient,
                doctor=doctor,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                status='Scheduled',
                reason=reason
            )
            
            messages.success(request, f'Appointment booked successfully! Your appointment ID is {new_id}')
            return redirect('dashboard')
            
        except Exception as e:
            messages.error(request, f'Error booking appointment: {str(e)}')
            return redirect('dashboard')
    
    return redirect('dashboard')
