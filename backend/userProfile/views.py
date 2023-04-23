import django.contrib.auth.decorators
from django.shortcuts import render,redirect
from django.contrib.auth import login 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

# Create your views here.
def vendor_detail(request,pk):
    user=User.objects.get(pk=pk)
    context={
        'user':user
    }
    return render(request, 'user_profile/vendor_detail.html',context)

def signup(request):
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
        
            user_profile=UserProfile.objects.create(user=user)
            return redirect('store:home')
    else:
        form=UserCreationForm()
    return render(request,'user_profile/signup.html',{'form':form})

@login_required
def my_account(request,id=None):
    

    return render(request,'user_profile/my_account.html')