from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect, reverse, get_object_or_404

from core.Utils.Access.decorators import manager_required, superuser_required
from core.User.models import User
from .forms import UserFilterForm
from .tables import UserTable


@manager_required
def users_list(request):
    users = User.objects.all()

    user_filter = UserFilterForm(request.GET, queryset=users)
    users = user_filter.qs
    table_body = UserTable(users)
    page = request.GET.get("page", 1)
    table_body.paginate(page=page, per_page=settings.ITEMS_PER_PAGE)

    table = {
        'pk': 'User Data Table',
        'body': table_body
    }
    table_filter = {
        'pk': 'User filter',
        'body': user_filter,
        'action': reverse('users-list'),
    }

    return render(request, 'Admin/User/user_list.html',
                  {'table': table,
                   'filter': table_filter})


@manager_required
def users_view(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    return render(request, 'Admin/User/user_view.html', {'user': user})


@superuser_required
def users_delete(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    messages.success(request, f'User {user.email} deleted')
    user.delete()
    return redirect(reverse('users-list'), host='admin')
