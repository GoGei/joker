from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from core.Privilege.models import PrivilegeMessage


class PrivilegeMessageForm(forms.ModelForm):
    message = forms.CharField(label='Privilege message text', max_length=1024, required=True,
                              widget=CKEditorUploadingWidget(config_name='admin',
                                                             attrs={'class': 'form-control'}))

    class Meta:
        model = PrivilegeMessage
        fields = ['message']

    def __init__(self, *args, **kwargs):
        self.privilege_user = kwargs.pop('privilege_user')
        super(PrivilegeMessageForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(PrivilegeMessageForm, self).save(commit=False)
        instance.privilege_user = self.privilege_user

        if commit:
            instance.save()

        return instance


class PrivilegeMessageAddForm(PrivilegeMessageForm):
    pass


class PrivilegeMessageEditForm(PrivilegeMessageForm):
    pass
