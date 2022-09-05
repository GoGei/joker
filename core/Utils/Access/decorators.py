from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from core.Utils.Access.user_check_functions import manager_check, superuser_check


def manager_required(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='/login/'):
    actual_decorator = user_passes_test(
        manager_check,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator


def superuser_required(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='/login/'):
    actual_decorator = user_passes_test(
        superuser_check,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator
