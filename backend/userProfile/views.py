import django.contrib.auth.decorators
from django.shortcuts import render,redirect
from django.contrib.auth import login 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile
from store.models import Product
from .forms import ProductForm
from django.contrib import messages
from django.utils.text import slugify

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
def my_account(request):
    

    return render(request,'user_profile/my_account.html')


@login_required(login_url='/login/',redirect_field_name='next')
def my_store(request):
    seller_products= request.user.products.exclude(status=Product.DELETED)
    context={
        "products":seller_products
    }
    return render(request,'user_profile/my_store.html',context)



@login_required(login_url='/login/',redirect_field_name='next')
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            title=request.POST.get('title')
            product=form.save(commit=False)
            product.added_by=request.user
            product.slug=slugify(title) 
            form.save()
            messages.success(request, 'Product was added')
            return redirect('userProfile:my_store')
    else:
        form = ProductForm()

    context = {"title":"Add Product" ,'form': form}
    return render(request, 'user_profile/product_form.html', context)
@login_required
def edit_product(request,id):
    product=Product.objects.filter(added_by=request.user).get(id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES,instance=product)
        if form.is_valid():
            title=request.POST.get('title')
            product=form.save(commit=False)
            product.added_by=request.user
            product.slug=slugify(title) 
            messages.success(request, 'The changes was saved.')
            form.save()
            return redirect('userProfile:my_store')
    else:
        form = ProductForm(instance=product)
    context = {
        "title":"Edit Product",
        'form': form,
        'product':product
        }
    return render(request, 'user_profile/product_form.html', context)

@login_required
def delete_product(request, id):
    print("hello entering page")
    product = Product.objects.filter(added_by=request.user).get(id=id)
    print(product.status)
    
    product.status = Product.DELETED 
    print(product.status)
    product.save()

    messages.success(request, 'The product was deleted!')

    return redirect('userProfile:my_store')

