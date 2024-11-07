# patients/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Patient, MedicalRecord

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'birth_date']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['diagnosis', 'visit_date', 'analysis_results', 'complaint', 'treatment']
        widgets = {
            'visit_date': forms.DateInput(format='%d.%m.%Y', attrs={'type': 'date'}),
        }
