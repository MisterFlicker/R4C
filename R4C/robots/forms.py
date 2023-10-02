from django import forms
from . import generating_info

class RobotForm(forms.Form):
    Robot_info = forms.CharField(widget=forms.Textarea, max_length=999)


class SecondRobotForm(forms.Form):
    Robot_info = forms.CharField(initial=generating_info.generate_info(), widget=forms.Textarea, max_length=999)