from django.views import View
from django.shortcuts import render,redirect
from quiz.forms import SignupForm,LoginForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages

def home(request):
    return render(request, 'quiz/HomePage.html')

class SignUpController(View):
    def get(self,request):
        form=SignupForm()
        return render(request,template_name='quiz/signup.html',context={'form':form})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                redirect('quiz:signup_page')
            user = User.objects.create_user(**form.cleaned_data)
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('quiz:list_courses')

        return redirect('quiz:signup_page')


class LoginController(View):
    def get(self,request):
        form=LoginForm()
        return render(request,template_name='quiz/login.html',context={'form':form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if ((user is not None) and (user.is_superuser)):
                login(request, user)
                return redirect('quiz:admin_home')
            elif user is not None :
                login(request,user)
                return redirect('quiz:list_courses')

        return redirect('quiz:login_page')


def logout_user(request):
    logout(request)
    return redirect('quiz:login_page')
