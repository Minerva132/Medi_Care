"""Generate all remaining templates for all entities"""
import os

BASE_DIR = r"f:\Python\medicare\templates\medicare"

# Generic templates for other entities
entities = {
    'doctor': {
        'title': 'Doctor',
        'icon': 'user-md',
        'fields': ['doctor_id', 'first_name', 'last_name', 'specialization', 'phone_number', 'years_experience', 'hospital_branch', 'email']
    },
    'appointment': {
        'title': 'Appointment',
        'icon': 'calendar-check',
        'fields': ['appointment_id', 'patient', 'doctor', 'appointment_date', 'appointment_time', 'reason_for_visit', 'status', 'notes']
    },
    'treatment': {
        'title': 'Treatment',
        'icon': 'notes-medical',
        'fields': ['treatment_id', 'appointment', 'treatment_type', 'description', 'cost', 'treatment_date']
    },
    'billing': {
        'title': 'Billing',
        'icon': 'file-invoice-dollar',
        'fields': ['bill_id', 'patient', 'treatment', 'bill_date', 'amount', 'payment_method', 'payment_status']
    }
}

for entity, config in entities.items():
    # List template
    list_template = f"""{{%extends 'medicare/base.html'%}}

{{%block title%}}{config['title']}s - Medicare{{%endblock%}}

{{%block content%}}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h1 class="h2 fw-bold"><i class="fas fa-{config['icon']} text-primary"></i> {config['title']}s</h1>
    <a href="{{%url '{entity}_create'%}}" class="btn btn-primary">
        <i class="fas fa-plus me-2"></i>Add {config['title']}
    </a>
</div>

<div class="card">
    <div class="card-body">
        <div class="row mb-4">
            <div class="col-md-6">
                <form method="get" class="search-box">
                    <input type="text" name="search" class="form-control" placeholder="Search..." value="{{{{search_query}}}}">
                    <i class="fas fa-search"></i>
                </form>
            </div>
        </div>
        
        <div class="table-responsive">
            <table class="table table-hover">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Details</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {{%for item in page_obj%}}
                    <tr>
                        <td>{{{{item.{entity}_id}}}}</td>
                        <td><a href="{{%url '{entity}_detail' item.{entity}_id%}}">{{{{item}}}}</a></td>
                        <td>{{%if item.status%}}<span class="badge bg-primary">{{{{item.status}}}}</span>{{%endif%}}</td>
                        <td>
                            <a href="{{%url '{entity}_detail' item.{entity}_id%}}" class="btn btn-sm btn-info">
                                <i class="fas fa-eye"></i>
                            </a>
                            <a href="{{%url '{entity}_update' item.{entity}_id%}}" class="btn btn-sm btn-warning">
                                <i class="fas fa-edit"></i>
                            </a>
                            <a href="{{%url '{entity}_delete' item.{entity}_id%}}" class="btn btn-sm btn-danger">
                                <i class="fas fa-trash"></i>
                            </a>
                        </td>
                    </tr>
                    {{%empty%}}
                    <tr>
                        <td colspan="4" class="text-center text-muted">No {entity}s found</td>
                    </tr>
                    {{%endfor%}}
                </tbody>
            </table>
        </div>
        
        {{%if page_obj.has_other_pages%}}
        <nav>
            <ul class="pagination justify-content-center">
                {{%if page_obj.has_previous%}}
                <li class="page-item">
                    <a class="page-link" href="?page={{{{page_obj.previous_page_number}}}}">Previous</a>
                </li>
                {{%endif%}}
                
                {{%for num in page_obj.paginator.page_range%}}
                <li class="page-item {{%if page_obj.number == num%}}active{{%endif%}}">
                    <a class="page-link" href="?page={{{{num}}}}">{{{{num}}}}</a>
                </li>
                {{%endfor%}}
                
                {{%if page_obj.has_next%}}
                <li class="page-item">
                    <a class="page-link" href="?page={{{{page_obj.next_page_number}}}}">Next</a>
                </li>
                {{%endif%}}
            </ul>
        </nav>
        {{%endif%}}
    </div>
</div>
{{%endblock%}}"""
    
    # Detail template
    detail_template = f"""{{%extends 'medicare/base.html'%}}

{{%block title%}}{config['title']} Details - Medicare{{%endblock%}}

{{%block content%}}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h1 class="h2 fw-bold"><i class="fas fa-{config['icon']} text-primary"></i> {config['title']} Details</h1>
    <div>
        <a href="{{%url '{entity}_update' {entity}.{entity}_id%}}" class="btn btn-warning">
            <i class="fas fa-edit me-2"></i>Edit
        </a>
        <a href="{{%url '{entity}_list'%}}" class="btn btn-secondary">
            <i class="fas fa-arrow-left me-2"></i>Back
        </a>
    </div>
</div>

<div class="card">
    <div class="card-header">Information</div>
    <div class="card-body">
        <table class="table table-borderless">
            {{%for field in {entity}._meta.fields%}}
            <tr>
                <th>{{{{field.verbose_name|title}}}}:</th>
                <td>{{{{field.value_to_string({entity})}}}}</td>
            </tr>
            {{%endfor%}}
        </table>
    </div>
</div>
{{%endblock%}}"""
    
    # Form template
    form_template = f"""{{%extends 'medicare/base.html'%}}

{{%block title%}}{{{{action}}}} {config['title']} - Medicare{{%endblock%}}

{{%block content%}}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h1 class="h2 fw-bold"><i class="fas fa-{config['icon']} text-primary"></i> {{{{action}}}} {config['title']}</h1>
    <a href="{{%url '{entity}_list'%}}" class="btn btn-secondary">
        <i class="fas fa-arrow-left me-2"></i>Back
    </a>
</div>

<div class="card">
    <div class="card-body">
        <form method="post">
            {{%csrf_token%}}
            <div class="row">
                {{%for field in form%}}
                <div class="col-md-6 mb-3">
                    {{{{field.label_tag}}}}
                    {{{{field}}}}
                    {{%if field.errors%}}
                    <div class="text-danger">{{{{field.errors}}}}</div>
                    {{%endif%}}
                </div>
                {{%endfor%}}
            </div>
            <button type="submit" class="btn btn-primary">
                <i class="fas fa-save me-2"></i>Save
            </button>
        </form>
    </div>
</div>
{{%endblock%}}"""
    
    # Delete confirmation template
    delete_template = f"""{{%extends 'medicare/base.html'%}}

{{%block title%}}Delete {config['title']} - Medicare{{%endblock%}}

{{%block content%}}
<div class="card">
    <div class="card-header bg-danger text-white">
        <i class="fas fa-exclamation-triangle"></i> Confirm Deletion
    </div>
    <div class="card-body">
        <p>Are you sure you want to delete this {entity}?</p>
        <p class="text-danger">This action cannot be undone!</p>
        <form method="post">
            {{%csrf_token%}}
            <button type="submit" class="btn btn-danger">
                <i class="fas fa-trash me-2"></i>Delete
            </button>
            <a href="{{%url '{entity}_list'%}}" class="btn btn-secondary">Cancel</a>
        </form>
    </div>
</div>
{{%endblock%}}"""
    
    # Write all templates
    with open(os.path.join(BASE_DIR, f"{entity}_list.html"), 'w') as f:
        f.write(list_template)
    print(f"Created {entity}_list.html")
    
    with open(os.path.join(BASE_DIR, f"{entity}_detail.html"), 'w') as f:
        f.write(detail_template)
    print(f"Created {entity}_detail.html")
    
    with open(os.path.join(BASE_DIR, f"{entity}_form.html"), 'w') as f:
        f.write(form_template)
    print(f"Created {entity}_form.html")
    
    with open(os.path.join(BASE_DIR, f"{entity}_confirm_delete.html"), 'w') as f:
        f.write(delete_template)
    print(f"Created {entity}_confirm_delete.html")

print("\nAll templates generated successfully!")
