from django import forms
from django.core.validators import RegexValidator


class CustomerForm(forms.Form):
    email = forms.CharField(
        max_length=255,
        validators=[RegexValidator(regex='^[A-Za-z0-9.]{1,}@[A-Za-z0-9.\-]{1,}\.[A-Za-z]{2,}$')]
    )


class SerialForm(forms.Form):
    robot_model = forms.CharField(max_length=2)
    robot_version = forms.CharField(max_length=2)
