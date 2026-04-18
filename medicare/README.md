# Medicare Management System 🏥

A comprehensive, full-stack web application for managing healthcare operations built with Django and modern web technologies. This system demonstrates DBMS concepts, CRUD operations, and provides a complete solution for managing patients, doctors, appointments, treatments, and billing.

![Django](https://img.shields.io/badge/Django-5.2-green)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🌟 Features

### Core Functionality
- **🔐 Authentication System**: Secure login/logout functionality with session management
- **📊 Interactive Dashboard**: Real-time statistics, charts, and key metrics visualization
- **👥 Patient Management**: Complete CRUD operations for patient records
- **👨‍⚕️ Doctor Management**: Manage doctor profiles with specializations and experience
- **📅 Appointment Scheduling**: Book, update, and track appointments with various statuses
- **💊 Treatment Records**: Comprehensive treatment tracking with cost management
- **💰 Billing System**: Invoice generation, payment tracking, and financial reports

### Advanced Features
- **🔍 Search & Filter**: Advanced search functionality across all entities
- **📄 Pagination**: Efficient data display with page navigation
- **📤 Data Export**: Export patient data to CSV and invoices to PDF
- **📈 Analytics & Charts**: Visual representation of data with Chart.js
- **🎨 Modern UI**: Clean, responsive design with smooth animations
- **⚡ Performance**: Optimized database queries with select_related and prefetch_related
- **📱 Responsive Design**: Mobile-friendly interface

## 🏗️ Project Structure

```
medicare/
├── data/                          # CSV data files
│   ├── patients.csv              # 50 patient records
│   ├── doctors.csv               # 10 doctor profiles
│   ├── appointments.csv          # 200 appointments
│   ├── treatments.csv            # 200 treatment records
│   └── billing.csv               # 200 billing records
├── medicare/                      # Django app
│   ├── models.py                 # Database models
│   ├── views.py                  # View functions
│   ├── forms.py                  # Form definitions
│   ├── urls.py                   # URL routing
│   ├── admin.py                  # Admin configuration
│   └── management/
│       └── commands/
│           └── import_data.py    # CSV import command
├── medicare_project/              # Project settings
│   ├── settings.py               # Configuration
│   ├── urls.py                   # Main URL configuration
│   └── wsgi.py                   # WSGI configuration
├── templates/                     # HTML templates
│   └── medicare/
│       ├── base.html             # Base template
│       ├── dashboard.html        # Dashboard
│       ├── login.html            # Login page
│       ├── patient_*.html        # Patient templates
│       ├── doctor_*.html         # Doctor templates
│       ├── appointment_*.html    # Appointment templates
│       ├── treatment_*.html      # Treatment templates
│       └── billing_*.html        # Billing templates
├── static/                        # Static files (CSS, JS, images)
├── db.sqlite3                    # SQLite database
├── manage.py                     # Django management script
├── pyproject.toml                # UV project configuration
└── README.md                     # This file
```

## 🛠️ Technology Stack

### Backend
- **Django 5.2**: Python web framework
- **SQLite3**: Database management system
- **Python 3.12**: Programming language

### Frontend
- **Bootstrap 5.3**: CSS framework
- **Font Awesome 6.4**: Icon library
- **Chart.js**: Data visualization
- **Custom CSS**: Modern, gradient-based styling

### Package Management
- **UV**: Fast Python package installer and resolver
- **Pandas**: Data manipulation for CSV import
- **ReportLab**: PDF generation for invoices

## 🚀 Installation & Setup

### Prerequisites
- Python 3.12 or higher
- UV package manager

### Step 1: Install UV (if not installed)
```bash
# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Step 2: Clone the Repository
```bash
cd f:\Python\medicare
```

### Step 3: Install Dependencies
UV automatically manages the virtual environment and installs dependencies:
```bash
# All dependencies are defined in pyproject.toml
# UV will auto-install when running commands
```

### Step 4: Run Migrations
```bash
uv run python manage.py migrate
```

### Step 5: Create Superuser
```bash
uv run python manage.py createsuperuser
# Username: admin
# Email: admin@medicare.com
# Password: [your-secure-password]
```

### Step 6: Import Sample Data
```bash
uv run python manage.py import_data
```

This will import:
- 50 Patients
- 10 Doctors
- 200 Appointments
- 200 Treatments
- 200 Billing Records

### Step 7: Run Development Server
```bash
uv run python manage.py runserver
```

Visit: `http://127.0.0.1:8000/`

## 📖 Usage Guide

### Login Credentials
- **Username**: admin
- **Password**: [the password you created]

### Dashboard Overview
The dashboard provides:
- Total count of patients, doctors, and appointments
- Revenue statistics (total, paid, pending)
- Appointment status distribution
- Top treatments
- Recent and upcoming appointments
- Interactive charts

### Managing Records

#### Patients
1. Navigate to **Patients** from the sidebar
2. **Add New**: Click "Add Patient" button
3. **Search**: Use search bar to find patients
4. **View Details**: Click on patient name
5. **Edit**: Click edit icon in actions column
6. **Delete**: Click delete icon (requires confirmation)
7. **Export**: Click "Export CSV" to download all patient data

#### Doctors
1. Navigate to **Doctors** from the sidebar
2. Filter by specialization
3. View doctor's appointment history
4. Manage doctor profiles

#### Appointments
1. Navigate to **Appointments**
2. Filter by status (Scheduled, Completed, Cancelled, No-show)
3. Filter by date range
4. View appointment details with patient and doctor information
5. Update appointment status

#### Treatments
1. Navigate to **Treatments**
2. Filter by treatment type
3. View treatment costs and descriptions
4. Link to associated appointments

#### Billing
1. Navigate to **Billing**
2. Filter by payment status (Paid, Pending, Failed)
3. Filter by payment method
4. **Generate Invoice PDF**: Click on billing detail, then "Export PDF"
5. Track revenue and payment history

## 🗄️ Database Schema

### Patient Model
- patient_id (PK)
- first_name, last_name
- gender, date_of_birth
- contact_number, email
- address
- registration_date
- insurance_provider, insurance_number

### Doctor Model
- doctor_id (PK)
- first_name, last_name
- specialization
- phone_number
- years_experience
- hospital_branch
- email

### Appointment Model
- appointment_id (PK)
- patient_id (FK)
- doctor_id (FK)
- appointment_date, appointment_time
- reason_for_visit
- status
- notes

### Treatment Model
- treatment_id (PK)
- appointment_id (FK)
- treatment_type
- description
- cost
- treatment_date

### Billing Model
- bill_id (PK)
- patient_id (FK)
- treatment_id (FK)
- bill_date
- amount
- payment_method
- payment_status

## 🎨 UI/UX Features

### Design Principles
- **Modern Gradient Sidebar**: Purple gradient with smooth hover effects
- **Card-Based Layout**: Clean, shadowed cards with hover animations
- **Color-Coded Status**: Visual indicators for different statuses
- **Responsive Grid**: Mobile-first design approach
- **Smooth Transitions**: CSS animations for better user experience
- **Icon Integration**: Font Awesome icons throughout the interface

### Color Scheme
- Primary: `#2563eb` (Blue)
- Success: `#10b981` (Green)
- Warning: `#f59e0b` (Orange)
- Danger: `#ef4444` (Red)
- Gradient: `#667eea` to `#764ba2` (Purple gradient)

## 🔧 Management Commands

### Import Data
```bash
uv run python manage.py import_data
```
Imports all CSV files from the `data/` directory into the database.

### Create Superuser
```bash
uv run python manage.py createsuperuser
```

### Run Development Server
```bash
uv run python manage.py runserver
```

### Make Migrations
```bash
uv run python manage.py makemigrations
```

### Apply Migrations
```bash
uv run python manage.py migrate
```

## 📦 Dependencies

All dependencies are managed through `pyproject.toml`:

```toml
[project]
dependencies = [
    "django>=5.2.8",
    "pillow>=11.1.0",
    "reportlab>=4.2.5",
    "pandas>=2.2.3",
    "python-dateutil>=2.9.0.post0",
]
```

### Key Packages
- **Django**: Web framework
- **Pillow**: Image processing (for future enhancements)
- **ReportLab**: PDF generation
- **Pandas**: CSV data processing
- **python-dateutil**: Date parsing utilities

## 🔐 Security Features

- CSRF protection enabled
- Session-based authentication
- Password hashing with Django's built-in system
- Login required decorators for protected views
- SQL injection protection through ORM

## 📊 DBMS Concepts Demonstrated

1. **Database Design**: Normalized schema with proper relationships
2. **Primary Keys**: Unique identifiers for each entity
3. **Foreign Keys**: Relationships between tables
4. **CRUD Operations**: Create, Read, Update, Delete
5. **Queries**: Filtering, searching, and sorting
6. **Aggregation**: COUNT, SUM for statistics
7. **Joins**: select_related and prefetch_related
8. **Data Import**: Bulk creation from CSV files
9. **Pagination**: Efficient data retrieval
10. **Indexing**: Optimized queries with proper indexes

## 🌐 API Endpoints

All endpoints require authentication:

### Authentication
- `GET /` - Login page
- `POST /` - Login submission
- `GET /logout/` - Logout

### Dashboard
- `GET /dashboard/` - Main dashboard

### Patients
- `GET /patients/` - List patients
- `GET /patients/<id>/` - Patient details
- `GET /patients/create/new/` - Create patient form
- `POST /patients/create/new/` - Create patient
- `GET /patients/<id>/update/` - Update patient form
- `POST /patients/<id>/update/` - Update patient
- `GET /patients/<id>/delete/` - Delete confirmation
- `POST /patients/<id>/delete/` - Delete patient
- `GET /export/patients/csv/` - Export CSV

### Similar patterns for:
- `/doctors/*`
- `/appointments/*`
- `/treatments/*`
- `/billing/*`

## 🎯 Future Enhancements

Potential features to add:
- [ ] Email notifications for appointments
- [ ] SMS reminders
- [ ] Doctor availability calendar
- [ ] Patient portal for self-service
- [ ] Medical history tracking
- [ ] Prescription management
- [ ] Lab results integration
- [ ] Analytics dashboard with more charts
- [ ] Multi-user roles (admin, doctor, receptionist)
- [ ] API endpoints for mobile app
- [ ] Real-time chat support
- [ ] Appointment booking widget

## 🐛 Troubleshooting

### Common Issues

**Issue**: Cannot import CSV data
**Solution**: Ensure CSV files are in the `data/` directory and have correct encoding (UTF-8)

**Issue**: Static files not loading
**Solution**: Run `uv run python manage.py collectstatic`

**Issue**: Database errors
**Solution**: Delete `db.sqlite3` and run migrations again

**Issue**: UV command not found
**Solution**: Reinstall UV or use full path to UV executable

## 👨‍💻 Development

### Adding New Features
1. Create models in `models.py`
2. Create forms in `forms.py`
3. Add views in `views.py`
4. Configure URLs in `urls.py`
5. Create templates
6. Run migrations

### Code Style
- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions
- Keep views focused and simple

## 📝 License

This project is for educational and demonstration purposes.

## 🤝 Contributing

This is a demonstration project. Feel free to fork and modify for your needs.

## 📞 Support

For issues or questions, please check:
1. This README file
2. Django documentation: https://docs.djangoproject.com/
3. UV documentation: https://docs.astral.sh/uv/

## ✨ Acknowledgments

- Django framework for robust backend
- Bootstrap for responsive UI
- Chart.js for data visualization
- Font Awesome for icons
- UV for modern Python package management

## 📈 Project Statistics

- **Lines of Code**: ~3000+
- **Templates**: 20+
- **Models**: 5
- **Views**: 40+
- **URL Patterns**: 40+
- **Sample Data**: 660 records

---

**Built with ❤️ using Django, Bootstrap, and UV Package Manager**

*For DBMS demonstration and educational purposes*
