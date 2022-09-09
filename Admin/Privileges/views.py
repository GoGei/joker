from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect, reverse, get_object_or_404

from core.Utils.Access.decorators import manager_required, superuser_required
from core.Privilege.models import PrivilegeUser
from .forms import PrivilegeUserFilterForm, PrivilegeUserAddForm
from .tables import PrivilegeUsersTable


@manager_required
def privilege_user_list(request):
    privilege_user = PrivilegeUser.objects.select_related('user').all().ordered()

    privileged_user_filter = PrivilegeUserFilterForm(request.GET, queryset=privilege_user)
    privilege_user = privileged_user_filter.qs
    table_body = PrivilegeUsersTable(privilege_user)
    page = request.GET.get("page", 1)
    table_body.paginate(page=page, per_page=settings.ITEMS_PER_PAGE)

    table = {
        'pk': 'Privilege user Data Table',
        'body': table_body
    }
    table_filter = {
        'pk': 'Privilege user filter',
        'body': privileged_user_filter,
        'action': reverse('privileged-user-list'),
    }

    return render(request, 'Admin/PrivilegeUser/privileged_user_list.html',
                  {'table': table,
                   'filter': table_filter})


@manager_required
def privilege_user_add(request):
    if '_cancel' in request.POST:
        return redirect(reverse('privileged-user-list'), host='admin')

    form_body = PrivilegeUserAddForm(request.POST or None)

    if form_body.is_valid():
        privileged_user = form_body.save()
        messages.success(request, f'Privilege user {privileged_user.user.label} added')
        return redirect(reverse('privileged-user-list'), host='admin')

    form = {
        'body': form_body,
        'buttons': {'save': True, 'cancel': True},
        'inline_form': True
    }

    return render(request, 'Admin/PrivilegeUser/privileged_user_add.html',
                  {'form': form})


@manager_required
def privilege_user_view(request, privileged_user_id):
    privileged_user = get_object_or_404(PrivilegeUser, pk=privileged_user_id)
    return render(request, 'Admin/PrivilegeUser/privileged_user_view.html', {'privileged_user': privileged_user})


@superuser_required
def privilege_user_delete(request, privileged_user_id):
    privileged_user = get_object_or_404(PrivilegeUser, pk=privileged_user_id)
    messages.success(request, f'Privilege user {privileged_user.user.label} deleted')
    privileged_user.delete()
    return redirect(reverse('privileged-user-list'), host='admin')
