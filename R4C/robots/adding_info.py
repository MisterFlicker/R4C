from .models import Robot


# добавление информации о роботе в систему
def add_info(form):
    if Robot.objects.filter(model=form['model'], version=form['version'], created=form['created']).exists():
        return False
    robot = Robot()
    n = 1
    while Robot.objects.filter(serial=form['model'] + form['version'] + str(n)).exists():
        n += 1
    robot.serial = form['model'] + form['version'] + str(n)
    robot.model = form['model']
    robot.version = form['version']
    robot.created = form['created']
    robot.save()
    return True