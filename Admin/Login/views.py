from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django_hosts import reverse
from core.Utils.Access.user_check_functions import manager_check

from .forms import LoginForm


def login_view(request):
    user = request.user
    if user.is_authenticated and manager_check(user):
        return redirect(reverse('admin-home'))

    initial = {'email': request.COOKIES.get('email', '')}
    form = LoginForm(request.POST or None, initial=initial)
    if form.is_valid():
        data = form.cleaned_data

        email = data.get('email')
        password = data.get('password')
        user = authenticate(email=email, password=password)
        if user is None:
            form.add_error(None, 'User with this email and password not found or inactive')
        elif (user.is_staff or user.is_superuser) and user.is_active:
            login(request, user)

            remember_me = data.get('remember_me')
            if not remember_me:
                request.session.set_expiry(0)
                request.session.modified = True

            response = HttpResponseRedirect(reverse('admin-home', host='admin'))
            response.set_cookie('email', user.email)
            return response
        elif not (user.is_staff or user.is_superuser):
            form.add_error(None, 'User is not a staff ot superuser')
        else:
            form.add_error(None, 'User is not logged in')

    return render(request, 'Admin/Login/login_view.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect(reverse('admin-login', host='admin'))
