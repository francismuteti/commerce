from django.shortcuts import render, get_object_or_404,redirect
from duka.models import *
from .models import *
from django.contrib.auth.decorators import login_required

from django.utils import timezone
from django.contrib.auth.models import User,auth
from django.conf import settings
from django.core.mail import send_mail,EmailMessage
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
from io import BytesIO


from django.template.loader import render_to_string

# Create your views here.

@login_required
def checkout(request):
    user = request.user
    profile = UserProfile.objects.get(user_id=user.id)

    cart = Cart.objects.filter(user_id=user.id)
    Count =cart.count()
    form =OrderForm(request.POST)
    total = 0
    discount = 0
    difference =0
    for items in cart:
        total += items.product.price * items.quantity
        discount +=items.product.discount_price * items.quantity
        difference = total - discount
    if request.method =='POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        
        email = request.POST['email']
        phone = request.POST['phone']
        location = request.POST['state-province']
    
        order = Order()
        order.first_name = first_name
        order.last_name = last_name
        order.phone = phone
        order.city = location
        order.total_payable = total
       
        order.email=email
        order.save()
        print('success')

        shopcart = Cart.objects.filter(user_id=user.id)
        for rs in shopcart:
           
            item = OrderItem()
            item.quantity =rs.quantity
            item.order_id = order.id
            item.price = rs.product.price
            item.product_id = rs.product.id
            item.amount = rs.amount
            item.save()
            product =Item.objects.get(id=rs.product.id)
            product.quantity_available -=rs.quantity
            product.save()

            
        subject = f'Your Order no. 2909{order.id} '
        message = f'Dear {order.first_name},\n\n' \
            f'Your order has been received!.\n'\
            f'Your order Reference is 2909{order.id}.\n'\
            f'Thank You for shopping at OnyiShop'
        from_email = settings.EMAIL_HOST_USER
        send_mail(subject,message,from_email,{order.email},fail_silently=False)

        shopcart.delete() 
        context = {'vo':0,'order':order}
        return render(request,'pages/order-complete.html',context)
    
    else:
        pass
           
    context = {'cart':cart,'form':form,'total':total,'disi':discount,'dif':difference,'vo':Count,'profile':profile,'user':user}

    return render(request,'pages/checkout.html',context)




def render_to_pdf(template_src,context={}):
    template = get_template(template_src)
    html = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")),result)
    if not pdf.err:
        return HttpResponse(result.getvalue(),content_type='application/pdf')
    return None

def GeneratePdf(request,order_id):
    order =get_object_or_404(Order,id=order_id)
    orderitem = OrderItem.objects.filter(order_id=order_id)
    context ={'order':order,'items':orderitem}
    pdf = render_to_pdf('pdf.html',context)
    if pdf:

        response = HttpResponse(pdf,content_type='application/pdf')
        filename= "invoice_%s.pdf" %("10444")
        content = "inline; filename='%s'"%(filename)
        download= request.GET.get("download")
        if download:
            content = "attachment; filename='%s'"%(filename)
        response['Content-Disposition']=content
        return response
    return HttpResponse("error")

def order_invoice(request,order_id):
    order =get_object_or_404(Order,id=order_id)
    orderitem = OrderItem.objects.filter(order_id=order_id)
    pdf= GeneratePdf(request,order_id)
    subject = f' Order no. 2909{order.id} Confirmed! '
    message = f'Dear {order.first_name},\n\n' \
            f'Your Order has been confirmed and an invoice has been sent!.\n'\
            f'Shipping is underway.\n'\
           
    from_email = settings.EMAIL_HOST_USER
    email = EmailMessage(subject,message,from_email,{order.email})
    email.attach(f'order_{order.id}.pdf',pdf,'application/pdf')
    email.send()
    return redirect('duka:shop')
        