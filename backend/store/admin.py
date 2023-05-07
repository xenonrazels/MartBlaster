from django.contrib import admin
from store.models import Category,Product,Main_Navigation,Order,OrderItem,FeaturedProduct

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Main_Navigation)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(FeaturedProduct)