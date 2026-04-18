from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Patients
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/<str:pk>/', views.patient_detail, name='patient_detail'),
    path('patients/create/new/', views.patient_create, name='patient_create'),
    path('patients/<str:pk>/update/', views.patient_update, name='patient_update'),
    path('patients/<str:pk>/delete/', views.patient_delete, name='patient_delete'),
    
    # Doctors
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('doctors/<str:pk>/', views.doctor_detail, name='doctor_detail'),
    path('doctors/create/new/', views.doctor_create, name='doctor_create'),
    path('doctors/<str:pk>/update/', views.doctor_update, name='doctor_update'),
    path('doctors/<str:pk>/delete/', views.doctor_delete, name='doctor_delete'),
    
    # Appointments
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/<str:pk>/', views.appointment_detail, name='appointment_detail'),
    path('appointments/create/new/', views.appointment_create, name='appointment_create'),
    path('appointments/<str:pk>/update/', views.appointment_update, name='appointment_update'),
    path('appointments/<str:pk>/delete/', views.appointment_delete, name='appointment_delete'),
    
    # Treatments
    path('treatments/', views.treatment_list, name='treatment_list'),
    path('treatments/<str:pk>/', views.treatment_detail, name='treatment_detail'),
    path('treatments/create/new/', views.treatment_create, name='treatment_create'),
    path('treatments/<str:pk>/update/', views.treatment_update, name='treatment_update'),
    path('treatments/<str:pk>/delete/', views.treatment_delete, name='treatment_delete'),
    
    # Billing
    path('billing/', views.billing_list, name='billing_list'),
    path('billing/<str:pk>/', views.billing_detail, name='billing_detail'),
    path('billing/create/new/', views.billing_create, name='billing_create'),
    path('billing/<str:pk>/update/', views.billing_update, name='billing_update'),
    path('billing/<str:pk>/delete/', views.billing_delete, name='billing_delete'),
    
    # Export
    path('export/patients/csv/', views.export_patients_csv, name='export_patients_csv'),
    path('export/billing/<str:pk>/pdf/', views.export_billing_pdf, name='export_billing_pdf'),
    
    # AI Diagnosis
    path('ai-diagnosis/', views.ai_diagnosis_view, name='ai_diagnosis'),
    path('ai-diagnosis/result/', views.ai_diagnosis_result, name='ai_diagnosis_result'),
    
    # User Appointment Booking
    path('book-appointment/', views.user_book_appointment, name='user_book_appointment'),
]
