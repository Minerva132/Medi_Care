# Medicare Management System - Database Schema

## Entity Relationship Diagram

```mermaid
erDiagram
    Patient ||--o{ Appointment : "has many"
    Patient ||--o{ Billing : "has many"
    Doctor ||--o{ Appointment : "handles"
    Appointment ||--o{ Treatment : "receives"
    Treatment ||--o{ Billing : "generates"
    
    Patient {
        string patient_id PK
        string first_name
        string last_name
        char gender
        date date_of_birth
        string contact_number
        text address
        date registration_date
        string insurance_provider
        string insurance_number
        email email
    }
    
    Doctor {
        string doctor_id PK
        string first_name
        string last_name
        string specialization
        string phone_number
        int years_experience
        string hospital_branch
        email email
    }
    
    Appointment {
        string appointment_id PK
        string patient_id FK
        string doctor_id FK
        date appointment_date
        time appointment_time
        string reason_for_visit
        string status
        text notes
        datetime created_at
        datetime updated_at
    }
    
    Treatment {
        string treatment_id PK
        string appointment_id FK
        string treatment_type
        text description
        decimal cost
        date treatment_date
    }
    
    Billing {
        string bill_id PK
        string patient_id FK
        string treatment_id FK
        date bill_date
        decimal amount
        string payment_method
        string payment_status
    }
```

## Detailed Schema Information

### Patient Entity
- **Primary Key**: `patient_id` (e.g., P001, P002, ...)
- **Gender Choices**: Male (M), Female (F), Other (O)
- **Computed Properties**:
  - `full_name`: Combines first_name and last_name
  - `age`: Calculates age from date_of_birth
- **Relationships**:
  - One-to-Many with Appointments
  - One-to-Many with Billing

### Doctor Entity
- **Primary Key**: `doctor_id` (e.g., D001, D002, ...)
- **Specializations**: Cardiology, Dermatology, Pediatrics, Oncology, Neurology, Orthopedics, Other
- **Computed Properties**:
  - `full_name`: Combines "Dr." + first_name + last_name
- **Relationships**:
  - One-to-Many with Appointments

### Appointment Entity
- **Primary Key**: `appointment_id` (e.g., A001, A002, ...)
- **Status Choices**: Scheduled, Completed, Cancelled, No-show
- **Reason Choices**: Checkup, Consultation, Follow-up, Emergency, Therapy
- **Foreign Keys**:
  - `patient_id` → Patient
  - `doctor_id` → Doctor
- **Relationships**:
  - Many-to-One with Patient
  - Many-to-One with Doctor
  - One-to-Many with Treatment
- **Ordering**: Latest appointments first (DESC by date and time)

### Treatment Entity
- **Primary Key**: `treatment_id` (e.g., T001, T002, ...)
- **Treatment Types**: X-Ray, MRI, ECG, Chemotherapy, Physiotherapy, Surgery, Laboratory
- **Foreign Keys**:
  - `appointment_id` → Appointment
- **Relationships**:
  - Many-to-One with Appointment
  - One-to-Many with Billing
- **Ordering**: Latest treatments first (DESC by treatment_date)

### Billing Entity
- **Primary Key**: `bill_id` (e.g., B001, B002, ...)
- **Payment Methods**: Cash, Credit Card, Debit Card, Insurance, Online
- **Payment Status**: Pending, Paid, Failed, Refunded
- **Foreign Keys**:
  - `patient_id` → Patient
  - `treatment_id` → Treatment
- **Relationships**:
  - Many-to-One with Patient
  - Many-to-One with Treatment
- **Ordering**: Latest bills first (DESC by bill_date)

## Data Flow Diagram

```mermaid
graph LR
    A[Patient Registration] --> B[Patient Record]
    C[Doctor Assignment] --> D[Doctor Record]
    B --> E[Schedule Appointment]
    D --> E
    E --> F[Appointment Record]
    F --> G[Provide Treatment]
    G --> H[Treatment Record]
    H --> I[Generate Bill]
    B --> I
    I --> J[Billing Record]
    
    style A fill:#667eea,stroke:#333,stroke-width:2px,color:#fff
    style C fill:#667eea,stroke:#333,stroke-width:2px,color:#fff
    style B fill:#48bb78,stroke:#333,stroke-width:2px,color:#fff
    style D fill:#48bb78,stroke:#333,stroke-width:2px,color:#fff
    style F fill:#f6ad55,stroke:#333,stroke-width:2px,color:#fff
    style H fill:#fc8181,stroke:#333,stroke-width:2px,color:#fff
    style J fill:#9f7aea,stroke:#333,stroke-width:2px,color:#fff
```

## System Architecture

```mermaid
graph TB
    subgraph "Frontend Layer"
        UI[User Interface]
        AdminDash[Admin Dashboard]
        UserDash[User Dashboard]
        AIDiag[AI Diagnosis]
    end
    
    subgraph "Application Layer"
        Views[Django Views]
        Auth[Authentication]
        AIModule[AI Diagnosis Module]
    end
    
    subgraph "Data Layer"
        Patient[(Patient)]
        Doctor[(Doctor)]
        Appointment[(Appointment)]
        Treatment[(Treatment)]
        Billing[(Billing)]
    end
    
    UI --> Views
    AdminDash --> Views
    UserDash --> Views
    AIDiag --> AIModule
    
    Views --> Auth
    Views --> Patient
    Views --> Doctor
    Views --> Appointment
    Views --> Treatment
    Views --> Billing
    
    AIModule --> Views
    
    style UI fill:#667eea,color:#fff
    style AdminDash fill:#667eea,color:#fff
    style UserDash fill:#667eea,color:#fff
    style AIDiag fill:#667eea,color:#fff
    style Views fill:#48bb78,color:#fff
    style Auth fill:#48bb78,color:#fff
    style AIModule fill:#f6ad55,color:#fff
    style Patient fill:#fc8181,color:#fff
    style Doctor fill:#fc8181,color:#fff
    style Appointment fill:#fc8181,color:#fff
    style Treatment fill:#fc8181,color:#fff
    style Billing fill:#fc8181,color:#fff
```

## User Journey Flow

```mermaid
stateDiagram-v2
    [*] --> Login
    Login --> AdminDashboard : Admin User
    Login --> UserDashboard : Regular User
    
    AdminDashboard --> ManagePatients
    AdminDashboard --> ManageDoctors
    AdminDashboard --> ManageAppointments
    AdminDashboard --> ManageTreatments
    AdminDashboard --> ManageBilling
    AdminDashboard --> AIDiagnosis
    
    UserDashboard --> ViewProfile
    UserDashboard --> BookAppointment
    UserDashboard --> ViewAppointments
    UserDashboard --> ViewBilling
    UserDashboard --> AIDiagnosis
    
    AIDiagnosis --> SelectSymptoms
    SelectSymptoms --> GetDiagnosis
    GetDiagnosis --> ViewResults
    ViewResults --> BookAppointment
    
    BookAppointment --> ManageAppointments
    ManageAppointments --> ProvideTreatment
    ProvideTreatment --> ManageTreatments
    ManageTreatments --> GenerateBill
    GenerateBill --> ManageBilling
    
    ManageBilling --> [*]
    ViewBilling --> [*]
```

## Appointment Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Scheduled : Create Appointment
    Scheduled --> Completed : Patient Arrives & Treatment Done
    Scheduled --> Cancelled : Patient Cancels
    Scheduled --> NoShow : Patient Doesn't Arrive
    Completed --> [*]
    Cancelled --> [*]
    NoShow --> [*]
```

## Billing Payment Flow

```mermaid
stateDiagram-v2
    [*] --> Pending : Bill Generated
    Pending --> Paid : Payment Successful
    Pending --> Failed : Payment Failed
    Failed --> Pending : Retry Payment
    Paid --> Refunded : Refund Requested
    Paid --> [*]
    Refunded --> [*]
```

## Database Statistics (Current Data)

- **Patients**: 50 records
- **Doctors**: 10 records
- **Appointments**: 200 records
- **Treatments**: 200 records
- **Billing**: 200 records

**Total Records**: 660

## Key Features

1. **Primary Keys**: All custom string-based IDs (P001, D001, A001, T001, B001)
2. **Cascade Deletion**: Deleting a parent record removes related records
3. **Choices/Enums**: Predefined options for gender, specializations, status, etc.
4. **Auto Timestamps**: Created_at and updated_at for appointments
5. **Computed Properties**: full_name and age calculated dynamically
6. **Ordering**: All models ordered by date/ID (latest first)
7. **Related Names**: Reverse relationship access (e.g., patient.appointments.all())

## Usage Examples

### Get all appointments for a patient
```python
patient = Patient.objects.get(patient_id='P001')
appointments = patient.appointments.all()
```

### Get all treatments from an appointment
```python
appointment = Appointment.objects.get(appointment_id='A001')
treatments = appointment.treatments.all()
```

### Get patient's total billing
```python
patient = Patient.objects.get(patient_id='P001')
total = sum(bill.amount for bill in patient.bills.all())
```

### Get doctor's completed appointments
```python
doctor = Doctor.objects.get(doctor_id='D001')
completed = doctor.appointments.filter(status='Completed')
```
