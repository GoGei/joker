from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect, reverse, get_object_or_404

from core.Utils.Access.decorators import superuser_required
from core.Privilege.models import PrivilegeUser
from .forms import PrivilegeMessageAddForm, PrivilegeMessageEditForm
from .tables import PrivilegeMessagesTable


@superuser_required
def privilege_message_list(request, privilege_user_id):
    privilege_user = PrivilegeUser.objects.get(pk=privilege_user_id)
    privilege_messages = privilege_user.privilegemessage_set.all()

    table_body = PrivilegeMessagesTable(privilege_messages)
    page = request.GET.get("page", 1)
    table_body.paginate(page=page, per_page=settings.ITEMS_PER_PAGE)

    table = {
        'title': 'Privilege Message Data Table',
        'body': table_body
    }

    return render(request, 'Admin/PrivilegeUser/PrivilegeMessage/privilege_message_list.html',
                  {'table': table,
                   'privilege_user': privilege_user})


@superuser_required
def privilege_message_add(request, privilege_user_id):
    privilege_user = PrivilegeUser.objects.get(pk=privilege_user_id)

    if '_cancel' in request.POST:
        return redirect(reverse('privilege-message-list', args=[privilege_user.pk]), host='admin')

    form_body = PrivilegeMessageAddForm(request.POST or None,
                                        privilege_user=privilege_user)

    if form_body.is_valid():
        privilege_message = form_body.save()
        messages.success(request, f'Privilege message {privilege_message.pk} added')
        return redirect(reverse('privilege-message-list', args=[privilege_user.pk]), host='admin')

    form = {
        'body': form_body,
        'buttons': {'save': True, 'cancel': True},
        'inline_form': True
    }

    return render(request, 'Admin/PrivilegeUser/PrivilegeMessage/privilege_message_add.html',
                  {'form': form,
                   'privilege_user': privilege_user})


@superuser_required
def privilege_message_edit(request, privilege_user_id, message_id):
    privilege_user = PrivilegeUser.objects.get(pk=privilege_user_id)
    privilege_message = get_object_or_404(privilege_user.privilegemessage_set, pk=message_id)

    if '_cancel' in request.POST:
        return redirect(reverse('privilege-message-list', args=[privilege_user.pk]), host='admin')

    form_body = PrivilegeMessageEditForm(request.POST or None,
                                         privilege_user=privilege_user,
                                         instance=privilege_message)

    if form_body.is_valid():
        privilege_message = form_body.save()
        messages.success(request, f'Privilege message {privilege_message.pk} edited')
        return redirect(reverse('privilege-message-list', args=[privilege_user.pk]), host='admin')

    form = {
        'body': form_body,
        'buttons': {'save': True, 'cancel': True},
        'inline_form': True
    }
    return render(request, 'Admin/PrivilegeUser/PrivilegeMessage/privilege_message_edit.html',
                  {'form': form,
                   'privilege_user': privilege_user})


@superuser_required
def privilege_message_view(request, privilege_user_id, message_id):
    privilege_user = PrivilegeUser.objects.get(pk=privilege_user_id)
    privilege_message = get_object_or_404(privilege_user.privilegemessage_set, pk=message_id)
    return render(request, 'Admin/PrivilegeUser/PrivilegeMessage/privilege_message_view.html',
                  {'privilege_message': privilege_message,
                   'privilege_user': privilege_user})


@superuser_required
def privilege_message_delete(request, privilege_user_id, message_id):
    privilege_user = PrivilegeUser.objects.get(pk=privilege_user_id)
    privilege_message = get_object_or_404(privilege_user.privilegemessage_set, pk=message_id)
    messages.success(request, f'Privilege message {privilege_message.pk} deleted')
    privilege_message.delete()
    return redirect(reverse('privilege-message-list', args=[privilege_user.pk]), host='admin')
