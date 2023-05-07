from django.http import JsonResponse
from django.shortcuts import render,redirect,get_object_or_404,reverse
from django.contrib import messages
import tensorflow
from django.contrib.auth.decorators import login_required
from io import BytesIO
from .models import Product,Category,Order,OrderItem,CartItem,FeaturedProduct
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from .cart import Cart 
from store.forms import OrderForm


# Load the VGG16 model and remove the last layer
# vgg_model = vgg16.VGG16(weights='imagenet', include_top=False)
# Create your views here.
model = MobileNetV2(weights='imagenet')
def index(request):
    products=Product.objects.filter(status=Product.ACTIVE)
    featured_products=FeaturedProduct.objects.all().filter(product__status=Product.ACTIVE)
    context={
        'products':products,
        'featured_products':featured_products
    }
    return render(request, 'front_page.html',context)

def product_detail(request,id):
    product=Product.objects.filter(status=Product.ACTIVE).get(id=id)
    cart=Cart(request)
    context={
        'product':product
    }
    return render(request, 'store/product_details.html',context)

def department_categories(request):
    categories=Category.objects.all()
    context={ 
        'categories':categories
    }
    return render(request, 'store/all_categories.html',context)

def category(request,slug):
    category=Category.objects.get(slug=slug)
    category_product=category.products.filter(status=Product.ACTIVE)
    context={
        'category':category,
        'products':category_product
    }
    return render(request, 'store/category.html',context)

def feature_extractor(img):
    model = MobileNetV2(weights='imagenet', include_top=False, pooling='avg')
    x = img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    features = model.predict(x)[0]
    return features

def search_product(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        if image:
            # Load the query image and extract features
            img_bytes = image.read()
            img = load_img(BytesIO(img_bytes), target_size=(224, 224))
            query_features = feature_extractor(img)

            # Retrieve all products from the database and compute similarities
            all_products = Product.objects.filter(status=Product.ACTIVE)
            similarities = []
            for product in all_products:
                # Load the image and extract features
                if product.image:
                    img_bytes = product.image.read()
                    img = load_img(BytesIO(img_bytes), target_size=(224, 224))
                    features = feature_extractor(img)

                    # Compute similarity between the query and the image
                    similarity = cosine_similarity(query_features.reshape(1, -1), features.reshape(1, -1))[0][0]
                    similarities.append((product, similarity))

            # Sort products by similarity and display the results
            sorted_products = sorted(similarities, key=lambda x: x[1], reverse=True)
            context = {
                'query': image,
                'products': [{'id': p.id, 'title': p.title, 'image': p.image.url, 'similarity': s} for p, s in sorted_products]
            }
            return render(request, 'store/search.html', context)
    else:
        # If the request method is not POST or an image was not uploaded, display the search form
        return render(request, 'front_page.html')






def cart(request):
    cart = Cart(request)
    return render(request, 'store/cart_view.html', {'cart': cart })

def change_quantity(request, product_id):
    action = request.GET.get('action', '')
        
    if action:
        quantity = 1

        if action == 'decrease':
            quantity = -1

        cart = Cart(request)
        cart.add(product_id, quantity, True)
    
    return redirect('store:cart_view')

def add_to_cart(request, product_id):

    cart = Cart(request)
    cart.add(product_id)
   
    return redirect(reverse('store:Product_detail',args=[product_id]))
def remove_from_cart(request, product_id):
    cart = Cart(request)
    print(cart)
    print(product_id)
    cart.remove(product_id)
    return redirect('store:cart_view')

@login_required(login_url='/login/',redirect_field_name='next')
def checkout_page(request):
    cart=Cart(request)
    total_price=cart.get_total_cost()
    if request.method == "POST":
        form=OrderForm(request.POST)
        if form.is_valid():
            
            for item in cart:
                product=item['product']
                total_price+=product.price*int (item['quantity'])
            order=form.save(commit=False)
            order.created_by=request.user
            order.paid_amount=total_price
            order.save()

            for item in cart:
                product=item['product']
                quantity=int(item['quantity'])
                price=product.price*quantity
                item=OrderItem.objects.create(order=order,product=product,quantity=quantity,price=price)
            cart.clear()
            messages.success(request, 'Your order is placed')

            return redirect("userProfile:my_account")
    else:
      
        form=OrderForm()
    
    context={
        'total_price':total_price,
        'form': form
    }

    return render(request,'store/checkout.html',context)