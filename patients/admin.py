from django.contrib import admin
from .models import Patient, MedicalRecord, MedicalRecordHashHistory


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'birth_date')
    search_fields = ('first_name', 'last_name')
    list_filter = ('birth_date',)


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'diagnosis', 'visit_date', 'modified_at', 'blockchain_hash')
    search_fields = ('diagnosis',)
    list_filter = ('visit_date',)


@admin.register(MedicalRecordHashHistory)
class MedicalRecordHashHistoryAdmin(admin.ModelAdmin):
    list_display = ('medical_record', 'blockchain_hash', 'timestamp')


class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'diagnosis', 'visit_date', 'is_modified')

    def is_modified(self, obj):
        return obj.has_data_changed()

    is_modified.boolean = True
    is_modified.short_description = 'Data Modified'

from .models import Patient, MedicalRecord, MedicalRecordHashHistory


