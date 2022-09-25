from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django_hosts import reverse

from core.User.models import User
from core.User.utils import RegistrationCodeHandler

from .forms import RegisterUserForm, RegisterUserResendForm


def register_view(request):
    if '_cancel' in request.POST:
        return redirect(reverse('home-index', host='public'))

    form_body = RegisterUserForm(request.POST or None)
    if form_body.is_valid():
        inactive_user = form_body.save()
        inactive_user.send_activation_mail(request=request)
        return render(request, 'Public/Register/registration_successful.html', {'user': inactive_user})
    else:
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user and not user.is_active:
            user.send_activation_mail(request=request)
            return render(request, 'Public/Register/registration_resend_activation.html', {'user': user})

    form = {
        'title': 'Please, register',
        'body': form_body,
        'buttons': {'save': True, 'cancel': True},
    }

    return render(request, 'Public/Register/registration.html', {'form': form})


def register_resend_view(request):
    if '_cancel' in request.POST:
        return redirect(reverse('home-index', host='public'))

    form_body = RegisterUserResendForm(request.POST or None)
    if form_body.is_valid():
        inactive_user = form_body.cleaned_data.get('user')
        inactive_user.send_activation_mail(request=request)
        return render(request, 'Public/Register/registration_resend_activation.html', {'user': inactive_user})

    form = {
        'title': 'Resend code',
        'body': form_body,
        'buttons': {'save': True, 'cancel': True},
    }

    return render(request, 'Public/Register/registration_resend.html', {'form': form})


def register_activate_view(request, user_pk, code):
    user = get_object_or_404(User, pk=user_pk)
    handler = RegistrationCodeHandler(user)

    try:
        user = handler.validate_registration_code(code)
        user.is_active = True
        user.save()
    except ValueError as e:
        return render(request, 'Public/Register/registration_activation_not_success.html', {'error_message': str(e)})

    login(request, user)
    return redirect(reverse('home-index', host='public'))
