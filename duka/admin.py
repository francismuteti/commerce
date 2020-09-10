from django.contrib import admin

# Register your models here.
from .models import *




class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','category','price','quantity_available','image']
    list_filter = ['category']

class CartAdmin(admin.ModelAdmin):
    list_display = ['product','user','quantity','price','amount']
    list_filter = ['user']
class MessageAdmin(admin.ModelAdmin):
    list_display = ['name','subject','email','status']
admin.site.register(Cart,CartAdmin)
admin.site.register(ContactMessage,MessageAdmin)
admin.site.register(Item,ProductAdmin)
admin.site.register(UserProfile)
