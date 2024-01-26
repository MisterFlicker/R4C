from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .models import Order
from R4C.customers.models import Customer
from .forms import CustomerForm, SerialForm
from R4C.robots.models import Robot
from django.core.mail import send_mail


@require_http_methods(['GET', 'POST'])
def orders(request):
    form1 = CustomerForm()
    form2 = SerialForm()

    if "delete" in request.POST:
        Order.objects.all().delete()

    if request.method == 'POST':
        if "send_email" in request.POST:
            cur_email = request.POST.get('email')
            cur_serial = request.POST.get('serial')
            send_mail(
                "Order is ready!",
                f"Добрый день!\nВы интересовались нашим роботом модели {cur_serial[0:2]}, версии {cur_serial[2:-1]}.\n"
                f"Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами",
                "webmaster@localhost",
                [f"{cur_email}"],
                fail_silently=False,
            )
            messages.error(request, "Email sent")

        if "create_order" in request.POST:
            form1 = CustomerForm(request.POST)
            form2 = SerialForm(request.POST)
            if form1.is_valid():
                if form2.is_valid():
                    new_email = Customer(email=form1.cleaned_data['email'])
                    new_email.save()

                    new_model = form2.cleaned_data['robot_model']
                    new_version = form2.cleaned_data['robot_version']
                    n = 1
                    while Order.objects.filter(robot_serial=new_model + new_version + str(n)).exists():
                        n += 1
                    new_order = Order(
                        customer=new_email,
                        robot_serial=new_model.upper() + new_version.upper() + str(n)
                    )
                    new_order.save()

                    messages.error(request, "Order is created")
                else:
                    messages.error(request, "Wrong format of robot's serial")
            else:
                messages.error(request, "Wrong format of email")

    ready_orders = []
    if Order.objects.only('customer', 'robot_serial').exists():
        for i in Order.objects.only('customer', 'robot_serial'):
            c_email = getattr(getattr(i, 'customer'), 'email')
            c_serial = getattr(i, 'robot_serial')
            if Robot.objects.filter(serial=c_serial).exists():
                ready_orders.append([c_email, c_serial])
    count_of_ready = len(ready_orders)

    return render(
        request,
        'orders.html',
        {'form1': form1, 'form2': form2, 'ready_orders': ready_orders, 'count_of_ready': count_of_ready}
    )
