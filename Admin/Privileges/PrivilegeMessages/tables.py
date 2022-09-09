import django_tables2 as tables
from core.Privilege.models import PrivilegeMessage


class PrivilegeMessagesTable(tables.Table):
    message = tables.TemplateColumn(template_name='Admin/PrivilegeUser/PrivilegeMessage/privilege_message_message_label.html', # noqa
                                    orderable=False)
    is_active = tables.BooleanColumn(orderable=False)
    actions = tables.TemplateColumn(template_name='Admin/PrivilegeUser/PrivilegeMessage/privilege_message_actions.html',  # noqa
                                    orderable=False)

    class Meta:
        model = PrivilegeMessage
        fields = ('pk', 'message', 'is_active', 'actions')
        template_name = "django_tables2/bootstrap4.html"
