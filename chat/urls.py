from django.urls import path
from . import views
from .views import CustomPasswordResetView, CustomPasswordResetDoneView, CustomPasswordResetConfirmView, CustomPasswordResetCompleteView

urlpatterns=[
    path('chat',views.chat, name='chat'),
    path('',views.login, name='login'),
    path('register',views.register, name='register'),
    path('logout',views.logout, name='logout'),
    path("ask_question/", views.ask_question, name="ask_question"),
    path('home', views.home, name='home'),
    path('premium/', views.premium, name='premium'),
    path('agreement/', views.agreement_view, name='agreement'),
    path('admission_upload',views.admission_upload, name='admission_upload'),
    path('admission_confirm',views.admission_confirm, name='admission_confirm'),
    path('admission_success',views.admission_success, name='admission_success'),


    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
]