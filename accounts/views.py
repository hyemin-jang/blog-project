from django.contrib.auth.forms import AuthenticationForm
from django.http.response import HttpResponse
from accounts.forms import SignupForm, LoginForm
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login #view 함수명 login과 구분하기위해
from django.contrib.auth import logout as auth_logout


def signup(request):
    if request.method =="POST": #폼이 POST데이터에 bind됨
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid(): #폼에 내장된 모든 유효성검증 규칙을 통과하면
            form.save() #forms.py 에서 지정한 함수
            return redirect('/admin/')
            
    else: 
        form = SignupForm() #unbound

    return render(request, 'accounts/signup.html' , {'form': form})


def login(request):
    if request.method == "POST":
        form = LoginForm(request, request.POST) #유저가 존재하는지 검증하는 장고 내장 폼
        #왜 인자가 request, request.POST 두개인가?
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('/admin/')
    else: 
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout(request):
    auth_logout(request)
    return redirect('/')



