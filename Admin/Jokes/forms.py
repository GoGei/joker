from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from core.Utils.filtersets import BaseFilterForm
from core.Joke.models import Joke


class JokeFilterForm(BaseFilterForm):
    SEARCH_FIELDS = ['text']

    class Meta:
        model = Joke
        fields = BaseFilterForm.BASE_FILTER_FIELDS


class JokeForm(forms.ModelForm):
    text = forms.CharField(label='Joke text', max_length=4096, required=True,
                           widget=CKEditorUploadingWidget(config_name='admin',
                                                          attrs={'class': 'form-control'}))

    class Meta:
        model = Joke
        fields = ['text']

    def clean_text(self):
        text = self.cleaned_data.get('text')
        instance = self.instance or None
        if not Joke.is_allowed_to_assign_slug(text, instance):
            self.add_error('text', 'With this text slug can not be assigned to joke. Please, change a text of joke!')
        return text

    def save(self, commit=True):
        instance = super(JokeForm, self).save(commit=commit)

        if commit:
            instance.assign_slug()
        return instance


class JokeAddForm(JokeForm):
    pass


class JokeEditForm(JokeForm):
    pass
