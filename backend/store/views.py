from django.shortcuts import render
import store.views
from io import BytesIO
from .models import Product,Category
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from keras.applications.mobilenet import preprocess_input, decode_predictions
# from tensorflow.keras.applications import vgg16
from keras.applications import MobileNet

# Load the VGG16 model and remove the last layer
# vgg_model = vgg16.VGG16(weights='imagenet', include_top=False)
# Create your views here.
def index(request):
    products=Product.objects.all()
    context={
        'products':products
    }

    return render(request, 'front_page.html',context)

def product_detail(request,id):
    product=Product.objects.get(id=id)
    context={
        'product':product
    }
    return render(request, 'store/product_details.html',context)

def department_categories(request):
    categories=Category.objects.all()
    print(categories)
    context={
        'categories':categories
    }
    return render(request, 'store/all_categories.html',context)

def category(request,slug):
    category=Category.objects.get(slug=slug)
    category_product=category.products.all()
    
    context={
        'category':category
    }
    return render(request, 'store/category.html',context)


def search_product(request):
    # query=request.GET['query']
    # products=Product.objects.filter(title__icontains=query)
    if request.method=='POST':
        query = request.POST.get('query', '')
        image=request.POST.get('image','')
        products = Product.objects.all()
        if image:
            # Load the image from the request
        
            img_bytes=BytesIO(image.read())
            img = load_img(img_bytes, target_size=(224, 224))
            x = img_to_array(img)
            x = np.expand_dims(x, axis=0)
            model = MobileNet(weights='imagenet')
            x = preprocess_input(x)
            # x = vgg16.preprocess_input(x)

            # Extract features from the image using the VGG16 model
            # features = vgg_model.predict(x)

            # # Compute the cosine similarities between the image features and the product features
            # product_features = np.array([p.features for p in Product.objects.all()])
            # similarities = np.dot(product_features, features.T) / (np.linalg.norm(product_features, axis=1) * np.linalg.norm(features))

            # Sort the products by similarity
            # sorted_indices = similarities.argsort()[0][::-1]
            # products = Product.objects.filter(id__in=[p.id for p in products])
            preds = model.predict(x)
            pred= decode_predictions(preds, top=3)[0]
            found_object=[ p[1] for p in pred]
            query=found_object 
            
        # Build a corpus of product titles
            corpus = [p.title   +" "+ p.description + " "+p.category.title for p in products]

        # Create a TF-IDF vectorizer
            vectorizer = TfidfVectorizer()

        # Compute the TF-IDF matrix for the corpus
            tfidf_matrix = vectorizer.fit_transform(corpus)

        # Compute the TF-IDF matrix for the query
            query_tfidf = vectorizer.transform(query)

        # Compute the cosine similarities between the query and the product titles
            similarities = cosine_similarity(query_tfidf, tfidf_matrix)
            print(similarities)

        # Sort the products by their similarity to the query
            sorted_indices = similarities.argsort()[0][::-1].tolist()
            sorted_products = [products[i] for i in sorted_indices]
            print(sorted_products)
            context = {
                'query': found_object,
                'products': sorted_products
            }
            return render(request, 'store/search.html', context)

        else:
            # If the request method is not POST or an image was not uploaded, display the search form
            return render(request, 'front_page.html')
            
        # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
   
        products = Product.objects.all()

        # Build a corpus of product titles
        corpus = [p.title  +" "+ p.description + " "+p.category.title for p in products]
        print(corpus)

        # Create a TF-IDF vectorizer
        vectorizer = TfidfVectorizer()

        # Compute the TF-IDF matrix for the corpus
        tfidf_matrix = vectorizer.fit_transform(corpus)

        # Compute the TF-IDF matrix for the query
        query_tfidf = vectorizer.transform([query])

        # Compute the cosine similarities between the query and the product titles
        similarities = cosine_similarity(query_tfidf, tfidf_matrix)
        print(similarities)

        # Sort the products by their similarity to the query
        sorted_indices = similarities.argsort()[0][::-1].tolist()
        sorted_products = [products[i] for i in sorted_indices]

        context = {
            'query': query,
            'products': sorted_products
        }

    return render(request, 'store/search.html', context)
    # context={
    #     'query':query,
    #     'products':products
    # }

    # return render(request,'store/search.html',context)
# def search_product_by_image(request):
#     if request.method == 'POST' and request.FILES.get('image'):
#         # Load the image from the request
#         img_file = request.FILES['image']
#         img = keras_image.load_img(img_file, target_size=(224, 224))
#         x = keras_image.img_to_array(img)
#         x = np.expand_dims(x, axis=0)
#         # x = vgg16.preprocess_input(x)
        


# # Load the MobileNet model
#        

# # Load an image and preprocess it for prediction
       



#         x = preprocess_input(x)

# # Make a prediction on the image
#         preds = model.predict(x)
#         print(preds[1]) 

# # Print the top 5 predicted classes
#         print('Predicted:', decode_predictions(preds, top=5)[0])

#         # Extract features from the image using the VGG16 model
       

#         # Compute the cosine similarities between the image features and the product features
#         # product_features = np.array([p.features for p in Product.objects.all()])
#         # similarities = np.dot(product_features, features.T) / (np.linalg.norm(product_features, axis=1) * np.linalg.norm(features))

#         # Sort the products by similarity
#         # sorted_indices = similarities.argsort()[0][::-1]

#         products = Product.objects.filter(id__in=[p.id for p in products])

        
#       

def search_product_by_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        print("i received the image")
        # Load the image from the request
        img_file = request.FILES['image']
        img_bytes=BytesIO(img_file.read())
        img = load_img(img_bytes, target_size=(224, 224))
        x = img_to_array(img)
        x = np.expand_dims(x, axis=0)
        model = MobileNet(weights='imagenet')
        x = preprocess_input(x)
        # x = vgg16.preprocess_input(x)

        # Extract features from the image using the VGG16 model
        # features = vgg_model.predict(x)
        

        # # Compute the cosine similarities between the image features and the product features
        # product_features = np.array([p.features for p in Product.objects.all()])
        # similarities = np.dot(product_features, features.T) / (np.linalg.norm(product_features, axis=1) * np.linalg.norm(features))

        # Sort the products by similarity
        # sorted_indices = similarities.argsort()[0][::-1]
        # products = Product.objects.filter(id__in=[p.id for p in products])
        preds = model.predict(x)
        pred= decode_predictions(preds, top=3)[0]
        found_object=[ p[1] for p in pred]
        print(found_object)
        products = Product.objects.all()

    # Build a corpus of product titles
        corpus = [p.title   +" "+ p.description + " "+p.category.title for p in products]
        print(corpus)

    # Create a TF-IDF vectorizer
        vectorizer = TfidfVectorizer()

    # Compute the TF-IDF matrix for the corpus
        tfidf_matrix = vectorizer.fit_transform(corpus)

    # Compute the TF-IDF matrix for the query
        query_tfidf = vectorizer.transform(found_object)

    # Compute the cosine similarities between the query and the product titles
        similarities = cosine_similarity(query_tfidf, tfidf_matrix)

    # Sort the products by their similarity to the query
        sorted_indices = similarities.argsort()[0][::-1].tolist()
        sorted_products = [products[i] for i in sorted_indices]
        print(sorted_products)
        context = {
            'query': found_object,
            'products': sorted_products
        }
        return render(request, 'store/search.html', context)
    else:
        # If the request method is not POST or an image was not uploaded, display the search form
        return render(request, 'front_page.html')
 