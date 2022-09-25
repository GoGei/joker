from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django_hosts import reverse

from .forms import LoginForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('home-index'))

    form = LoginForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data

        email = data.get('email')
        password = data.get('password')
        user = authenticate(email=email, password=password)
        if user is None:
            form.add_error(None, 'User with this email and password not found or inactive')
        elif user.is_active:
            login(request, user)

            response = HttpResponseRedirect(reverse('home-index', host='public'))
            response.set_cookie('email', user.email)
            return response
        else:
            form.add_error(None, 'User is not logged in')

    return render(request, 'Public/Home/public_login_view.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect(reverse('home-index', host='public'))
