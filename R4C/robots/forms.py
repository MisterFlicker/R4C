from django import forms
from django.core.validators import RegexValidator
from .models import Document


class RobotForm(forms.Form):
    model = forms.CharField(initial='', max_length=2, validators=[RegexValidator(regex='^[A-Z0-9]{2}$')])
    version = forms.CharField(initial='', max_length=2, validators=[RegexValidator(regex='^[A-Z0-9]{2}$')])
    created = forms.CharField(
        initial='',
        max_length=19,
        validators=[RegexValidator(regex='^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}$')]
    )


class UploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('document', )
