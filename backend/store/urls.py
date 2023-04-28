from django.urls import re_path ,path 
from store.views import index,product_detail,department_categories,category,search_product,cart,add_to_cart


app_name='store'

urlpatterns=[
    path('',index,name='home'),
    path('product/<int:id>',product_detail,name='Product_detail'),
    path('department-categories/',department_categories,name='Department_Categories'),
    path('category/<str:slug>/',category,name='category_detail'),
    path('search/',search_product,name='search_product'),
    path('cart/',cart,name='cart_view'),
    path('add_to_cart/<int:product_id>/',add_to_cart,name='add_to_cart'),
]
