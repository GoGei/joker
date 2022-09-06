import django_tables2 as tables
from core.User.models import User


class UserTable(tables.Table):
    actions = tables.TemplateColumn(template_name='Admin/User/user_actions.html', orderable=False)

    class Meta:
        model = User
        fields = ('email', 'is_active', 'is_staff', 'is_superuser', 'actions')
        template_name = "django_tables2/bootstrap4.html"
