from django.contrib import admin
from django.utils.safestring import mark_safe

# Register your models here.
from .models import *

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    can_delete= False
    extra = 0
    readonly_Fields = ['product','price','qantity','amount']
class OrderAdmin(admin.ModelAdmin):
    def order_pdf(obj):
        url = reverse('orders:admin_order_pdf', args=[obj.id])
        return mark_safe(f'<a href="{url}">PDF</a>')
    order_pdf.short_description = 'Invoice'
    list_display = ['first_name','last_name','email','city','phone','paid','ordered_date',order_pdf]
    inlines = [OrderItemInline]

admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem)