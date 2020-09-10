from django.db import models

# Create your models here.
from duka.models import *

class Order(models.Model):
   
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email =models.EmailField(max_length=50,blank=True,null=True)
   
    
    city = models.CharField(max_length=100)
    paid = models.BooleanField(default=False)
    phone =models.CharField(max_length=50)
    total_payable = models.DecimalField(max_digits=10, decimal_places=2)
   
    def get_invoice(self):
        return reverse('orders:send_invoice',args=[self.id])
   
    def __str__(self):
        return self.first_name
class OrderForm(ModelForm):
     class Meta:
        model = Order
        fields = ['first_name','last_name','city','phone','email','phone','total_payable']


class OrderItem(models.Model):
    
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Item,on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return self.product.title
        
        

    