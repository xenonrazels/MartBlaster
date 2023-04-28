from django.http import JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
import tensorflow
from io import BytesIO
from .models import Product,Category
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from .cart import Cart 

# Load the VGG16 model and remove the last layer
# vgg_model = vgg16.VGG16(weights='imagenet', include_top=False)
# Create your views here.
model = MobileNetV2(weights='imagenet')
def index(request):
    products=Product.objects.filter(status=Product.ACTIVE)
    context={
        'products':products
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


def search_product(request):
    # query=request.GET['query']
    # products=Product.objects.filter(title__icontains=query)
    if request.method=='POST':
        query = [request.POST.get('query', '')]
        image=request.FILES.get('image','')
        products = Product.objects.all()
        if image :
            print("hello recived")
            # Load the image from the request
            img_bytes=BytesIO(image.read())
            img = load_img(img_bytes, target_size=(224, 224))
            print(" kernal (224 )")
            x = img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)
            preds = model.predict(x)
            pred= decode_predictions(preds, top=3)
           
            if pred:
                for pred_list in pred:
                    for label, desc, prob in pred_list:
                       
                        query.append(desc)
                query=str(query)
          
    # Build a corpus of product titles
        corpus = [p.title   +" "+ p.description  + " "+p.category.title for p in products]

    # Create a TF-IDF vectorizer
        vectorizer = TfidfVectorizer()

    # Compute the TF-IDF matrix for the corpus
        tfidf_matrix = vectorizer.fit_transform(corpus)

    # Compute the TF-IDF matrix for the query
        query_tfidf = vectorizer.transform([query])

    # Compute the cosine similarities between the query and the product titles
        similarities = cosine_similarity(query_tfidf, tfidf_matrix)
        # Sort the products by their similarity to the query
        sorted_indices = similarities.argsort()[0][::-1].tolist()
        sorted_products = [products[i] for i in sorted_indices]
        context = {
            'query': query,
            'products': sorted_products
        }
        return render(request, 'store/search.html', context)
    else:
        # If the request method is not POST or an image was not uploaded, display the search form
        return render(request, 'front_page.html')


def cart(request):
    cart = Cart(request)
    return render(request, 'store/cart_view.html', {'cart': cart })

def add_to_cart(request, product_id):
    print(f'we got the add_tocart ,{product_id}')
    cart = Cart(request)
    cart.add(product_id)
    cart_count = len(cart)
    response_data = {'cart_count': cart_count, 'product_id': product_id}
    return JsonResponse(response_data)