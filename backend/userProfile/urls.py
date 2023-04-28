from django.urls import path
from userProfile.views import signup,my_account
from userProfile.views import my_store
from userProfile.views import add_product,edit_product,delete_product
from .views import vendor_detail 
from django.contrib.auth import views as auth_views


app_name='userProfile'

urlpatterns=[
    path('vendors/<int:pk>', vendor_detail,name='vendor_detail'),
    path('signup/', signup,name='signup'),
    path('login/',auth_views.LoginView.as_view(template_name='user_profile/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('my_account/', my_account,name='my_account'),
    path('my_store/', my_store,name='my_store'),
    path('add_product/',add_product,name='add_product'),
    path('edit_product/<int:id>/',edit_product,name='edit_product'),
    path('delete_product/<int:id>/',delete_product,name='delete_product'),
]