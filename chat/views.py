from django.shortcuts import render,redirect
from django.http import JsonResponse
import openai
import json
from django.contrib import auth 
from django.contrib.auth.models import User
from .models import Chat
from django.utils import timezone

from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView


def ask_openai(message):
    response =openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages=[
                {"role": "system",
                "content": """
                
                write in Json Format, you are only amental health assistant
                **AVAILABLE_THERAPIES:** Please provide information about available therapies for managing mental health effectively.
                **SELF_CARE_TECHNIQUES:** Offer techniques and exercises for self-care for managing mental health effectively.
                **SUMMARY_REPORT:** Must Generate a brief report on the service offered.
                """
            },
    {"role": "user", "content": message},
    
  ]

    )


    
    answer =response.choices[0].message.content.strip()
    return answer
# Create your views here.
def chatbot(request):
    chats  =Chat.objects.filter(user=request.user)
    if request.method=='POST':
        message = request.POST.get('message')
        response = ask_openai(message)


        chat=Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'message':message, 'response':response})
    return render(request, 'chatbot.html',{'chats':chats})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('chatbot')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        error_message = None 
        return render(request, 'login.html', {'error_message': error_message})



def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if not User.objects.filter(email=email).exists():
                try:
                    user = User.objects.create_user(username, email, password1)
                    auth.login(request, user)
                    return render(request, 'registration_success.html')  
                except:
                    error_message = 'Enter a valid email'
            else:
                error_message = 'Email already exists'
        else:
            error_message = 'Passwords do not match'

        return render(request, 'register.html', {'error_message': error_message})

    return render(request, 'register.html')


def logout(request):
    auth.logout(request)
    return redirect('login')

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