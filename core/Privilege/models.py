from django.db import models
from core.Utils.Mixins.models import CrmMixin


class PrivilegeUser(CrmMixin):
    user = models.OneToOneField('User.User', on_delete=models.CASCADE, db_index=True)

    class Meta:
        db_table = 'privilege_user'

    def __str__(self):
        return f'{self.user.label}'

    @property
    def label(self):
        return f'Privileged user {self.user.label}'


class PrivilegeMessage(models.Model):
    privilege_user = models.ForeignKey(PrivilegeUser, on_delete=models.CASCADE)
    message = models.CharField(max_length=1024)

    class Meta:
        db_table = 'privilege_message'

    @property
    def label(self):
        return f'Message for user {self.privilege_user.user.label}'
