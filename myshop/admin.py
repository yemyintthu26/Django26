from django.contrib import admin
from myshop.models import Category, Product, Order, Cart
# Register your models here.

class PorductAdmin(admin.ModelAdmin):
    list_display = ['id','name','image','category','qty','price','created_at']

admin.site.register(Category)
admin.site.register(Product, PorductAdmin)
admin.site.register(Order)
admin.site.register(Cart)
