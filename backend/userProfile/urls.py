from django.urls import path
from userProfile.views import signup,my_account
from .views import vendor_detail 
from django.contrib.auth import views as auth_views


app_name='userProfile'

urlpatterns=[
    path('vendors/<int:pk>', vendor_detail,name='vendor_detail'),
    path('signup/', signup,name='vendor_detail'),
    path('login/',auth_views.LoginView.as_view(template_name='user_profile/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('my_account/', my_account,name='my_account'),

]