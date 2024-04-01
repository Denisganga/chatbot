from django.shortcuts import render,redirect
from django.http import JsonResponse
import openai
import json
from django.contrib import auth 
from django.contrib.auth.models import User
from .models import Chat
from django.utils import timezone




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
        error_message = None  # Initialize error_message to None when rendering the login page
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
                return redirect('chatbot')
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