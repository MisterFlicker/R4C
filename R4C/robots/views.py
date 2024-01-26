from django.shortcuts import render
from django.views.decorators.http import require_http_methods
import json
from .forms import RobotForm, UploadForm
from django.contrib import messages
from .adding_info import add_info, validate_file
from .models import Robot
from .making_report import make_report, dates
from . import generating_info
import glob
import os


@require_http_methods(['POST'])
def upload_file(request):
    form = RobotForm()
    file_form = UploadForm(request.POST, request.FILES)
    if file_form.is_valid():
        file_form.save()
        list_of_files = glob.glob('./media/documents/*')
        latest_file = max(list_of_files, key=os.path.getctime)
        print(latest_file)
        if latest_file.split('.')[-1] in ('txt', 'json'):
            with open(latest_file) as f:
                data = json.load(f)
                if validate_file(data):
                    for key, value in data.items():
                        form[f'{key}'].initial = value
                else:
                    messages.error(request, "Incorrect format of info in file")
        else:
            messages.error(request, "Incorrect extension of file")

    return render(request, 'robots.html', {'form': form, 'file_form': file_form})


@require_http_methods(['POST'])
def report(request):
    if "make_report" in request.POST:
        week = dates()
        week_robots = Robot.objects.filter(created__range=(week['begin'], week['end'])).only('model', 'version').distinct('model', 'version')
        return make_report(week_robots)


@require_http_methods(['GET', 'POST'])
def robots(request):
    form = RobotForm()
    file_form = UploadForm()
    if request.method == 'POST':
        if "generate_info" in request.POST:
            for key, value in generating_info.generate_info().items():
                form[f'{key}'].initial = value

        if "delete" in request.POST:
            Robot.objects.all().delete()

        if "upload_info" in request.POST:
            form = RobotForm(request.POST)

            if form.is_valid():
                r_model = form.cleaned_data['model'].upper()
                r_version = form.cleaned_data['version'].upper()
                r_created = form.cleaned_data['created']
                if add_info(r_model, r_version, r_created):
                    messages.error(request, "Info added to system")
                else:
                    messages.error(request, "Info about this robot already exists in system")
            else:
                messages.error(request, "Wrong format of robot info")

    return render(request, 'robots.html', {'form': form, 'file_form': file_form})