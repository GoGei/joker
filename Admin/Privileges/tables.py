import django_tables2 as tables
from core.Privilege.models import PrivilegeUser


class PrivilegeUsersTable(tables.Table):
    user = tables.TemplateColumn(template_name='Admin/PrivilegeUser/privileged_user_user_label.html', orderable=True)
    actions = tables.TemplateColumn(template_name='Admin/PrivilegeUser/privileged_user_actions.html', orderable=False)

    class Meta:
        model = PrivilegeUser
        fields = ('user', 'actions')
        template_name = "django_tables2/bootstrap4.html"
