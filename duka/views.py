from django.shortcuts import render, get_object_or_404,redirect
from .models import *
from django.http import JsonResponse
from django.contrib import messages
import json


from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from django.utils import timezone
from django.contrib.auth.models import User,auth
# Create your views here.


def home(request):
    user = request.user

    cart = Cart.objects.filter(user_id=user.id)
    Count =cart.count()
    item = Item.objects.all()
 
    context={'product':item,'vo':Count}
    
    return render(request,'index.html',context)

def cartPage(request):
    user = request.user

    cart = Cart.objects.filter(user_id=user.id)
    Count =cart.count()
    total = 0
    discount = 0
    difference = 0
    for items in cart:
        total += items.product.price * items.quantity
        discount +=items.product.discount_price * items.quantity
        difference = total - discount
    context = {'cart':cart,'total':total,'disi':discount,'dif':difference,'vo':Count}

    return render(request,'pages/cart.html',context)
@login_required(login_url = '/login')
def AddToCart(request,id):
    
    user = request.user
    productCheck = Cart.objects.filter(product_id=id)
    if productCheck:
        control =1
    else:
        control = 0
    if request.method == 'POST':
        form = CartForm(request.POST)
        if form.is_valid():
            if control ==1:
                data = Cart.objects.get(product_id=id)
                data.quantity += form.cleaned_data['quantity']
                data.save()
            else:
                data = Cart()
                data.user_id = user.id
                data.product_id = id
                data.quantity = form.cleaned_data['quantity']
                data.save()
               
            return redirect('duka:shop')
            print('product adedd')
    else:
        if control ==1:
            data = Cart.objects.get(product_id=id)
            data.quantity += 1
            data.save()
        else:
            data = Cart()
            data.user_id = user.id
            data.product_id = id
            data.quantity = 1
            data.save()

        messages.success(request, 'product added')
        print('product added')
        return redirect('duka:shop')


def removeFromCart(request,id):
    Cart.objects.filter(product_id=id).delete()
    return redirect('duka:cart')
def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password2==password1:
            if User.objects.filter(username=username).exists():
                return redirect('duka:login')

            else:
               
                user = User.objects.create_user(username=username, first_name=first_name,last_name=last_name,email=email,password=password2)
                user.save()
                
           
                
                return redirect('duka:login')
                
        else:
            return redirect('duka:login')
    return render(request,'pages/register.html')

def logout(request):
    auth.logout(request)
    return redirect('duka:shop')
def login(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password1']
        user = auth.authenticate(username=username,password=password)
       
        if user is not None:
            auth.login(request, user)
            if UserProfile.objects.filter(user_id=user.id).exists():
                return redirect('duka:shop')
            else:
                return redirect('duka:update-profile')
                
        else:
            return redirect('duka:shop')
    return render(request,'pages/login.html')


def shopGrid(request):
    user = request.user

    cart = Cart.objects.filter(user_id=user.id)
    Count =cart.count()
    item = Item.objects.all()
  
    context={'items':item,'vo':Count}
    return render(request,'pages/shop-grid.html',context)


def updateProfile(request):
    
    user = request.user
    profile=None

    try:
        profile = UserProfile.objects.get(user_id=user.id)
    except UserProfile.DoesNotExist:
        pass
    if request.method=='POST':
        phone = request.POST['number']
        location = request.POST['state-province']
        if UserProfile.objects.filter(phone=phone).exists():
                return redirect('duka:shop')

        else:
            
            current_user= request.user
            
            
            profile = UserProfile()
            profile.user_id=current_user.id
            profile.city =location
            profile.phone=phone

            profile.save()
        
            
            return redirect('duka:shop')
            
         

    context = {'user':user,'profile':profile}
  
    return render(request,'profile.html',context)

def Contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        subject = request.POST['subject']
        email = request.POST['email']
        message = request.POST['message']
          
        feedback = ContactMessage.objects.create(name=name,subject=subject,email=email,message=message)
        feedback.save() 
        return redirect('/')

    else:
        return render(request,'pages/contact.html')
def product(request,id):
    user = request.user

    cart = Cart.objects.filter(user_id=user.id)
    Count =cart.count()
    products= get_object_or_404(Item, id=id)
    
    context={'product':products,'vo':Count}
    return render(request,'product-page.html',context)
