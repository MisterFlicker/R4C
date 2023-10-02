from django.http import HttpResponse
from datetime import date, timedelta
from .models import Robot
from io import BytesIO
import xlsxwriter


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