from django.contrib import admin
from ecomapp.models import Product


# admin.site.register(Product)

class ProductAdmin(admin.ModelAdmin):
    
    list_display = ['id','name','price','cat','pdetail','is_active']
    list_filter = ['id', 'is_active']
admin.site.register(Product,ProductAdmin)
