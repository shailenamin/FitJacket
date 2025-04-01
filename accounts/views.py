from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .forms import CustomUserCreationForm, CustomErrorList
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings


@login_required
def logout(request):
    auth_logout(request)
    return redirect('home.index')


def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET':
        return render(request, 'accounts/login.html', {'template_data': template_data})
    elif request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            template_data['error'] = 'The username or password is incorrect.'
            return render(request, 'accounts/login.html', {'template_data': template_data})
        else:
            auth_login(request, user)
            return redirect('home.index')


def signup(request):
    template_data = {}
    template_data['title'] = 'Sign up'
    if request.method == 'GET':
        template_data['form'] = CustomUserCreationForm
        return render(request, 'accounts/signup.html', {'template_data': template_data})
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
        if form.is_valid():
            user = form.save()
            send_mail(
                "Welcome to FitJacket!",
                f"Hi {user.username},\n\nWelcome to FitJacket! We are glad to see you here!",
                "fitjacket.ian2@gmail.com",
                [user.email],
                fail_silently=False,
            )
            return redirect('accounts.login')
        else:
            template_data['form'] = form
            return render(request, 'accounts/signup.html', {'template_data': template_data})


def resetPassword(request):
    template_data = {}
    template_data['title'] = 'Reset Password'
    if request.method == 'GET':
        return render(request, 'accounts/resetPassword.html', {'template_data': template_data})
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
        return redirect('accounts.login')


@login_required
def orders(request):
    template_data = {}
    template_data['title'] = 'Orders'
    template_data['orders'] = request.user.order_set.all()
    return render(request, 'accounts/orders.html',
                  {'template_data': template_data})