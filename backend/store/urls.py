from django.urls import re_path ,path 
from store.views import index,product_detail,department_categories,category,search_product
from store.views import search_product_by_image

app_name='store'

urlpatterns=[
    path('',index,name='home'),
    path('product/<int:id>',product_detail,name='Product_detail'),
    path('department-categories/',department_categories,name='Department_Categories'),
    path('category/<str:slug>/',category,name='category_detail'),
    path('search/',search_product,name='search_product'),
     path('search_by_image/',search_product_by_image,name='search_product'),
]
