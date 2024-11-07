# patients/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PatientForm, MedicalRecordForm
from .models import Patient, MedicalRecord
from django.shortcuts import render, get_object_or_404
from .models import MedicalRecord, MedicalRecordHashHistory
from django.shortcuts import render, get_object_or_404
from .models import Patient, MedicalRecord

def create_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm()
    return render(request, 'patients/create_patient.html', {'form': form})

def create_medical_record(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.patient = patient
            record.save()
            return redirect('patient_detail', patient_id=patient.id)
    else:
        form = MedicalRecordForm()
    return render(request, 'patients/create_medical_record.html', {'form': form, 'patient': patient})

def check_records(request):
    modified_records = MedicalRecord.validate_all_records()
    return render(request, 'check_records.html', {'modified_records': modified_records})
def patient_list(request):
    # Отримуємо значення пошукового запиту з GET-запиту
    query = request.GET.get('q')

    # Якщо є пошуковий запит, фільтруємо пацієнтів за ім'ям або прізвищем
    if query:
        patients = Patient.objects.filter(first_name__icontains=query) | Patient.objects.filter(
            last_name__icontains=query)
    else:
        # Якщо немає запиту, відображаємо всіх пацієнтів
        patients = Patient.objects.all()

    context = {
        'patients': patients,
    }

    return render(request, 'patients/patient_list.html', context)
def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'patients/patient_list.html', {'patients': patients})

def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    records = MedicalRecord.objects.filter(patient=patient)
    return render(request, 'patients/patient_detail.html', {'patient': patient, 'records': records})

def home(request):
    return render(request, 'patients/home.html')

def delete_medical_record(request, record_id, patient_id):
    record = get_object_or_404(MedicalRecord, id=record_id)
    record.delete()
    return redirect('patient_detail', patient_id=patient_id)

def view_patient_hash_chain(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    records = MedicalRecord.objects.filter(patient=patient).order_by('visit_date', 'id')



