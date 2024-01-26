from .models import Robot
import cerberus


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