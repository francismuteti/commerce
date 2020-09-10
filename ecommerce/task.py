import celery
from .celery import app as celery_app
from orders.models import Order
from celery import task
from django.core.mail import send_mail


@task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    message = f'Dear {order.first_name},\n\n' \
              f'Your order was succesfully created.'\
              f'Your order Reference is {order.id}.'
    mail_sent=send_mail(subject,message,'mutetimuteti888@gmail.com',{order.email})

    return mail_sent