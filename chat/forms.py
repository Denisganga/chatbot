# forms.py
from django import forms
from .models import AdmissionDocument

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = AdmissionDocument
        fields = ['result_slip', 'birth_certificate', 'admission_letter', 'preferred_path']
