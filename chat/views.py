from django.shortcuts import render,redirect
from django.http import JsonResponse
import openai
import json
from django.contrib import auth 
from django.contrib.auth.models import User
from .models import Chat
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

# views.py
from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from .models import ChatBot
from django.http import HttpResponseRedirect, JsonResponse
import google.generativeai as genai

# Create your views here.
# add here to your generated API key
genai.configure(api_key="AIzaSyCm9GYI3_F1K-VtI3BQ1b6shzvteIG02ys")

@login_required
def ask_question(request):
    if request.method == "POST":
        text = request.POST.get("text")

        # Set up the AI model and start a new chat
        model = genai.GenerativeModel("gemini-pro")
        chat = model.start_chat()

        # Combine pre-prompt and user message
        pre_prompt = (
    "You can only answer CBC related questions"
    "You are a CBC Pathway Helper specializing in guiding students through the Competency-Based Curriculum (CBC) pathway selection process. "
    "In lower secondary school, you assist students in choosing one of three available pathways. When students proceed to senior secondary school, they will specialize in their chosen pathway. "
    "The three CBC pathways are as follows and explain a small brief of pathway:\n"
    "1. Arts and Sports Science – Focused on creative and athletic fields, providing foundational and specialized skills in arts, culture, and sports.\n"
    "2. Social Sciences – Emphasizes human behavior, society, and the world, preparing students for roles in social service, education, and humanities.\n"
    "3. Science, Technology, Engineering, and Mathematics (STEM) – Concentrates on scientific and technical disciplines, ideal for students interested in innovation, problem-solving, and applied sciences.\n\n"
    "For each pathway, explain:\n"
    "- The core subjects required.\n"
    "- Optional subjects that students may choose to enhance their skills.\n"
    "- Potential future careers that students may pursue in this pathway.\n\n"
    "Answer clearly, with detailed information about each pathway’s subjects and future career opportunities, so that students and their families can make informed decisions."
        )
        combined_message = f"{pre_prompt}\n\nUser: {text}"

        # Send the combined pre-prompt and user question
        response = chat.send_message(combined_message)

        user = request.user

        # Prepare the response data for the client
        response_data = {
            "text": response.text,
        }
        return JsonResponse({"data": response_data})
    else:
        return HttpResponseRedirect(reverse("chat"))  # Redirect for GET requests


@login_required
def chat(request):
    user = request.user
    chats = ChatBot.objects.filter(user=user)
    return render(request, "chatbot.html", {"chats": chats})

# views.py
from django.shortcuts import render

def agreement_view(request):
    return render(request, 'agreement.html')

def premium(request):
    return render(request, 'premium.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        error_message = None 
        return render(request, 'login.html', {'error_message': error_message})



def register(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']

        if password1==password2:
            try:
                user=User.objects.create_user(username,email,password1)
                user.save()
                auth.login(request,user)
                return redirect('home')
            except:
                error_message='Error creating account'
                return render(request, 'register.html', {'error_message':error_message})
        else:
            error_message = 'password dont match'
            return render(request,'register.html', {'error_message':error_message})

    return render(request,'register.html')

def logout(request):
    auth.logout(request)
    return redirect('login')
def home(request):
    return render(request, 'home.html')
#password resetting

class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_reset_form.html'
    email_template_name = 'password_reset_email.html'
    success_url = '/password_reset/done/'

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    success_url = '/password_reset/complete/'

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'

# views.py
from django.shortcuts import render, redirect
from .forms import DocumentUploadForm
from .models import AdmissionDocument
from .ocr_processing import process_documents
from django.urls import reverse

def admission_upload(request):
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save()
            extracted_data = process_documents(document)  
            extracted_data['preferred_path'] = form.cleaned_data.get('preferred_path')

            request.session['extracted_data'] = extracted_data  
            
            return redirect(reverse('admission_confirm'))  # Redirect to confirmation page
    else:
        form = DocumentUploadForm()
    
    return render(request, 'admission_upload.html', {'form': form})

def admission_confirm(request):
    extracted_data = request.session.get('extracted_data', {})
    if request.method == 'POST':
        # Save the confirmed data to the database
        AdmissionDocument.objects.create(
            result_slip=extracted_data.get('result_slip'),
            birth_certificate=extracted_data.get('birth_certificate'),
            admission_letter=extracted_data.get('admission_letter'),
            preferred_path=extracted_data.get('preferred_path')
        )
        return redirect('admission_success') 
    
    return render(request, 'admission_confirm.html', {'extracted_data': extracted_data})

def admission_success(request):
    return render(request, 'admission_success.html')

