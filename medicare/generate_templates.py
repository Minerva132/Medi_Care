"""
Script to generate all remaining Django templates for the Medicare webapp
"""

import os

# Base directory
BASE_DIR = r"f:\Python\medicare\templates\medicare"

# Template definitions
templates = {
    "patient_detail.html": '''{% extends 'medicare/base.html' %}

{% block title %}Patient Details - Medicare{% endblock %}

{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h1 class="h2 fw-bold"><i class="fas fa-user text-primary"></i> Patient Details</h1>
    <div>
        <a href="{% url 'patient_update' patient.patient_id %}" class="btn btn-warning">
            <i class="fas fa-edit me-2"></i>Edit
        </a>
        <a href="{% url 'patient_list' %}" class="btn btn-secondary">
            <i class="fas fa-arrow-left me-2"></i>Back
        </a>
    </div>
</div>

<div class="row g-4">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header">Personal Information</div>
            <div class="card-body">
                <table class="table table-borderless">
                    <tr><th>Patient ID:</th><td>{{ patient.patient_id }}</td></tr>
                    <tr><th>Name:</th><td>{{ patient.full_name }}</td></tr>
                    <tr><th>Gender:</th><td>{{ patient.get_gender_display }}</td></tr>
                    <tr><th>Date of Birth:</th><td>{{ patient.date_of_birth }}</td></tr>
                    <tr><th>Age:</th><td>{{ patient.age }} years</td></tr>
                    <tr><th>Email:</th><td>{{ patient.email }}</td></tr>
                    <tr><th>Contact:</th><td>{{ patient.contact_number }}</td></tr>
                    <tr><th>Address:</th><td>{{ patient.address }}</td></tr>
                </table>
            </div>
        </div>
    </div>
    
    <div class="col-md-6">
        <div class="card">
            <div class="card-header">Insurance Information</div>
            <div class="card-body">
                <table class="table table-borderless">
                    <tr><th>Provider:</th><td>{{ patient.insurance_provider }}</td></tr>
                    <tr><th>Number:</th><td>{{ patient.insurance_number }}</td></tr>
                    <tr><th>Registration Date:</th><td>{{ patient.registration_date }}</td></tr>
                </table>
            </div>
        </div>
    </div>
</div>

<div class="row g-4 mt-2">
    <div class="col-md-12">
        <div class="card">
            <div class="card-header">Appointments</div>
            <div class="card-body">
                <table class="table table-hover">
                    <thead>
                        <tr><th>ID</th><th>Doctor</th><th>Date</th><th>Time</th><th>Status</th></tr>
                    </thead>
                    <tbody>
                        {% for apt in appointments %}
                        <tr>
                            <td>{{ apt.appointment_id }}</td>
                            <td>{{ apt.doctor.full_name }}</td>
                            <td>{{ apt.appointment_date }}</td>
                            <td>{{ apt.appointment_time }}</td>
                            <td><span class="badge bg-primary">{{ apt.status }}</span></td>
                        </tr>
                        {% empty %}
                        <tr><td colspan="5" class="text-center">No appointments</td></tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',

    "patient_form.html": '''{% extends 'medicare/base.html' %}

{% block title %}{{ action }} Patient - Medicare{% endblock %}

{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h1 class="h2 fw-bold"><i class="fas fa-user text-primary"></i> {{ action }} Patient</h1>
    <a href="{% url 'patient_list' %}" class="btn btn-secondary">
        <i class="fas fa-arrow-left me-2"></i>Back
    </a>
</div>

<div class="card">
    <div class="card-body">
        <form method="post">
            {% csrf_token %}
            <div class="row">
                <div class="col-md-6 mb-3">
                    {{ form.patient_id.label_tag }}
                    {{ form.patient_id }}
                </div>
                <div class="col-md-6 mb-3">
                    {{ form.first_name.label_tag }}
                    {{ form.first_name }}
                </div>
                <div class="col-md-6 mb-3">
                    {{ form.last_name.label_tag }}
                    {{ form.last_name }}
                </div>
                <div class="col-md-6 mb-3">
                    {{ form.gender.label_tag }}
                    {{ form.gender }}
                </div>
                <div class="col-md-6 mb-3">
                    {{ form.date_of_birth.label_tag }}
                    {{ form.date_of_birth }}
                </div>
                <div class="col-md-6 mb-3">
                    {{ form.contact_number.label_tag }}
                    {{ form.contact_number }}
                </div>
                <div class="col-md-12 mb-3">
                    {{ form.address.label_tag }}
                    {{ form.address }}
                </div>
                <div class="col-md-6 mb-3">
                    {{ form.email.label_tag }}
                    {{ form.email }}
                </div>
                <div class="col-md-6 mb-3">
                    {{ form.registration_date.label_tag }}
                    {{ form.registration_date }}
                </div>
                <div class="col-md-6 mb-3">
                    {{ form.insurance_provider.label_tag }}
                    {{ form.insurance_provider }}
                </div>
                <div class="col-md-6 mb-3">
                    {{ form.insurance_number.label_tag }}
                    {{ form.insurance_number }}
                </div>
            </div>
            <button type="submit" class="btn btn-primary">
                <i class="fas fa-save me-2"></i>Save
            </button>
        </form>
    </div>
</div>
{% endblock %}''',

    "patient_confirm_delete.html": '''{% extends 'medicare/base.html' %}

{% block title %}Delete Patient - Medicare{% endblock %}

{% block content %}
<div class="card">
    <div class="card-header bg-danger text-white">
        <i class="fas fa-exclamation-triangle"></i> Confirm Deletion
    </div>
    <div class="card-body">
        <p>Are you sure you want to delete patient <strong>{{ patient.full_name }}</strong>?</p>
        <p class="text-danger">This action cannot be undone!</p>
        <form method="post">
            {% csrf_token %}
            <button type="submit" class="btn btn-danger">
                <i class="fas fa-trash me-2"></i>Delete
            </button>
            <a href="{% url 'patient_list' %}" class="btn btn-secondary">Cancel</a>
        </form>
    </div>
</div>
{% endblock %}''',
}

# Create templates
for filename, content in templates.items():
    filepath = os.path.join(BASE_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created: {filename}")

print("\nAll patient templates created successfully!")
