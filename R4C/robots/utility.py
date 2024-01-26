import cerberus
import random
import string
from datetime import datetime, timedelta, date
from django.http import HttpResponse
from .models import Robot
from io import BytesIO
import xlsxwriter


# добавление информации о роботе в систему
def add_info(model, version, created):
    if Robot.objects.filter(model=model, version=version, created=created).exists():
        return False
    robot = Robot()
    n = 1
    while Robot.objects.filter(serial=model + version + str(n)).exists():
        n += 1
    robot.serial = model + version + str(n)
    robot.model = model
    robot.version = version
    robot.created = created
    robot.save()
    return True


def validate_file(data):
    schema = {'model': {'type': 'string', 'maxlength': 2},
              'version': {'type': 'string', 'maxlength': 2},
              'created': {'type': 'string', 'regex': r'^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}$'}}
    v = cerberus.Validator(schema)
    if v.validate(data):
        return True
    else:
        return False


# генерация случайной даты для случайной записи ниже
def generate_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    result = start + timedelta(seconds=random_second)
    return result


# генерация случайной записи об изготовленном роботе, которого еще нет в базе данных
def generate_info():
    letters = string.ascii_uppercase + string.digits
    date1 = datetime.strptime('1/1/1000 00:00:01', '%m/%d/%Y %H:%M:%S')
    date2 = datetime.strptime('1/1/9999 00:00:01', '%m/%d/%Y %H:%M:%S')

    rand_model = ''.join(random.choice(letters) for i in range(2))
    rand_version = ''.join(random.choice(letters) for i in range(2))
    rand_date = generate_date(date1, date2)

    rand_info = {
        'model': rand_model,
        'version': rand_version,
        'created': rand_date
    }

    return rand_info


# определение границ текущей недели
def dates():
    current_date = date.today()
    begin_of_week = current_date - timedelta(days=7)
    return {'begin': begin_of_week, 'end': current_date}


# создание excel-отчета о произведенных роботах за последнюю неделю
def make_report(week_robots):
    week = dates()
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    center = workbook.add_format({'align': 'center'})
    worksheet = ''
    x = 1
    y = 1

    for i in week_robots:

        if x != getattr(i, 'model'):
            x = getattr(i, 'model')
            worksheet = workbook.add_worksheet(getattr(i, 'model'))
            worksheet.write('A1', 'Модель', center)
            worksheet.write('B1', 'Версия', center)
            worksheet.write('C1', 'Количество за неделю', center)
            worksheet.autofit()
            y = 1

        worksheet.write(y, 0, getattr(i, 'model'), center)
        worksheet.write(y, 1, getattr(i, 'version'), center)
        worksheet.write(y, 2,
                        Robot.objects.filter(created__range=(week['begin'], week['end']),
                                             model=getattr(i, 'model'),
                                             version=getattr(i, 'version')).count(),
                        center)
        y += 1

    workbook.close()
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename="fixtures/42.xlsx"'
    response.write(output.getvalue())
    return response
