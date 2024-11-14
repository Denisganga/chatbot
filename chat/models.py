from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Chat(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    message=models.TextField()
    response=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}:{self.message}'
from django.db import models
from django.conf import settings

class ChatBot(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="gemini_users",  # Changed related_name to follow PEP8 naming conventions
        null=True
    )
    text_input = models.CharField(max_length=500)
    gemini_output = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.text_input
class AdmissionDocument(models.Model):
    result_slip = models.FileField(upload_to='documents/result_slips/')
    birth_certificate = models.FileField(upload_to='documents/birth_certificates/')
    admission_letter = models.FileField(upload_to='documents/admission_letters/')
    preferred_path = models.CharField(max_length=100, choices=[
        ('STEM', 'STEM'),
        ('Arts and Sports Science', 'Arts and Sports Science'),
        ('Social Sciences', 'Social Sciences'),
    ], null=True, blank=True)

    def __str__(self):
        return f"AdmissionDocument {self.id}"
