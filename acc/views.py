from django.shortcuts import render,redirect
from .forms import register,loginform
from .utils import get_otp
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from movies.models import Movie


# Create your views here.

def registerview(request):
    f=register()
    context={
        'form':f
    }
    if request.method=='POST':
        user=register(data =request.POST)
        if user.is_valid():
            user.save()
            username=user.cleaned_data['username']
            email=user.cleaned_data['email']
            send_mail(
                'Registration succesfully',
                f'{username} you have created account in movie ticket booking application',
                'adityaaa4689@gmail.com',
                [email],
                fail_silently=False
            )
            messages.success(request,"Mail Sent Successfully")
            messages.success(request,"Account Created Successfully")
            return redirect('login')
    return render(request,'accounts/register.html',context)





def sigin(request):
    fm=loginform()
    context={
        'form':fm
    }
    if request.method=='POST':
        fm=loginform(data=request.POST)
        if fm.is_valid():
            username=fm.cleaned_data['username']
            password=fm.cleaned_data['password']
            user_object=authenticate(request,username=username,password=password)
            if user_object is not None:
                if user_object.is_authenticated:
                    login(request,user_object)
                    messages.success(request,"logged in successfully")
                    return redirect('home')
            
        
    return render(request,'accounts/signin.html',context)


def logoutview(request):
    logout(request)
    messages.error(request,"Logout Successfull")
    return redirect('login')

                


