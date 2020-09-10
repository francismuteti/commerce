from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.forms import ModelForm
from coupon.models import Coupon



CATEGORY_CHOICES = (
    ('S', 'Shirt'),
    ('SW', 'Sport wear'),
    ('OW', 'Outwear'),
    ('C', 'Cars'),
    ('G', 'Groceries'),
    ('B','Beer'),
    ('SH','Shoes')
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)


class UserProfile(models.Model):
    user = models.OneToOneField(User,
                             on_delete=models.CASCADE,null=True)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(blank=True,max_length=20)
    city = models.CharField(blank=True,max_length=20)
    
    def __str__(self):
        return self.phone


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField()
    available = models.BooleanField(default=True)
    additional_info=models.TextField(max_length=300,blank=True)
    quantity_available = models.IntegerField(default=1)
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('duka:details',args=[self.id])
    def get_add_url(self):
        return reverse('duka:cart_add',args=[self.id])
    def get_remove_url(self):
        return reverse('duka:cart_remove',args=[self.id])
   
    @property
    def imageUrl(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url 

class ContactMessage(models.Model):
    STATUS =(
        ('New','New'),
        ('Read','Read'),
    )
    name = models.CharField(max_length=200)
    email =models.EmailField(max_length=50,blank=True,null=True)
    subject = models.CharField(max_length=50)
    message = models.TextField(max_length=500)
    status = models.CharField(choices=STATUS,default='New',max_length=30)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
class ContactForm(ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name','email','subject','message']

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    product = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity= models.IntegerField(default=1)
   

    
    def __str__(self):
        return self.product.title
  

    @property
    def price(self):
        return self.product.price
    
    @property
    def amount(self):
        if self.product.discount_price:
            return self.quantity * self.product.discount_price
        else:
            return self.quantity * self.product.price

    
class CartForm(ModelForm):
    class Meta:
        model = Cart
        fields = ['quantity']