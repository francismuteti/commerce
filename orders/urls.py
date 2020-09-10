from django.urls import path
from . import views


app_name ='orders'
urlpatterns = [
    path('checkout/',views.checkout, name='checkout'),
    path('admin/order/<int:order_id>/pdf/',views.GeneratePdf,name='admin_order_pdf'),
    path('confirm/<int:order_id>/Order/',views.order_invoice,name='send_invoice'),

]