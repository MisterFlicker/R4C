from django.shortcuts import render
from django.views.decorators.http import require_http_methods
import json
from .forms import RobotForm, SecondRobotForm
import cerberus
from django.contrib import messages
from datetime import datetime
from .adding_info import add_info
from .models import Robot
from .making_report import make_report, dates


@require_http_methods(['POST'])
def report(request):
    if "make_report" in request.POST:
        week = dates()
        week_robots = Robot.objects.filter(created__range=(week['begin'], week['end'])).only('model', 'version').distinct('model', 'version')
        return make_report(week_robots)


@require_http_methods(['GET', 'POST'])
def robots(request):
    form = RobotForm()

    if request.method == 'POST':
        if "generate_info" in request.POST:
            form = SecondRobotForm()

        if "delete" in request.POST:
            Robot.objects.all().delete()

        if "upload_info" in request.POST:
            form = RobotForm(request.POST)

            if form.is_valid():
                r_info = form.cleaned_data['Robot_info']
                try:
                    r_info = json.loads(r_info)
                except:
                    messages.error(request, "Wrong format of robot info")
                r_model = r_info['model']
                r_version = r_info['version']
                r_created = datetime.strptime(r_info['created'], '%Y-%m-%d %H:%M:%S')
                info = {'model': r_model, 'version': r_version, 'created': r_created}

                # схема для валидации входных данных
                schema = {'model': {'type': 'string'},
                          'version': {'type': 'string'},
                          'created': {'type': 'datetime'}}
                v = cerberus.Validator(schema)

                if v.validate(info):
                    if add_info(info):
                        messages.error(request, "Info added to system")

                    else:
                        messages.error(request, "Info about this robot already exists in system")
            else:
                messages.error(request, "Wrong format of robot info")

    return render(request, 'robots.html', {'form': form})