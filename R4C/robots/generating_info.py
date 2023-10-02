import random
import string
from datetime import datetime, timedelta


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

    rand_model = '{"model":"' + rand_model + '",\n'
    rand_version = '"version":"' + rand_version + '",\n'
    rand_created = '"created":"' + rand_date.strftime("%Y-%m-%d %H:%M:%S") + '"'
    rand_info = rand_model + rand_version + rand_created + '}'
    return rand_info