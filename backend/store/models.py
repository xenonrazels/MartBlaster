from django.db import models
from django.contrib.auth.models import User
from io import BytesIO
from PIL import Image
from django.core.files import File
from userProfile.models import Pasal
from django.core.validators import MaxValueValidator


class Main_Navigation(models.Model):
    title=models.CharField(max_length=100)
    slug=models.SlugField(unique=True)
    ordering = models.IntegerField(default=0)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name='Main Navigation'
        verbose_name_plural="Main Navigations"
        ordering = ['ordering']

# Create your models here.
class Category(models.Model):
    title=models.CharField(max_length=200)
    slug=models.SlugField(unique=True)
    ordering = models.IntegerField(default=0)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name='Category'
        verbose_name_plural="Categories"
        ordering = ['ordering']

 
class Product(models.Model):
    DRAFT = 'draft'
    WAITING_APPROVAL = 'waitingapproval'
    ACTIVE = 'active'
    DELETED = 'deleted'
    STATUS_CHOICES = (
        (DRAFT, 'Draft'),
        (WAITING_APPROVAL, 'Waiting approval'),
        (ACTIVE, 'Active'),
        (DELETED, 'Deleted'),
    )
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    vendor = models.ForeignKey(Pasal, related_name='products', on_delete=models.CASCADE,null=True)
    added_by=models.ForeignKey(User,related_name='products',on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=ACTIVE)

    class Meta:
        ordering = ['-date_added']
    
    def __str__(self):
        return f'{self.title } {self.status}'
    
    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return self.thumbnail.url
            else:
                return 'https://via.placeholder.com/240x180.jpg'
    
    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)
        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)
        thumbnail = File(thumb_io, name=image.name)

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class Order(models.Model):
    ORDERED='ordered'
    PACKAGING='packagig'
    SHIPPED='shipped]'
    STATUS_CHOICES=(
        ( ORDERED,'Ordered'),
        (  PACKAGING,'Packaging'),
        ( SHIPPED,'Shipped'),
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    paid_amount = models.IntegerField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    payment_intent = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, related_name='orders', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default=ORDERED)

    def __str__(self):
        return f'{self.created_by} :- at {self.created_at} {self.status}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)
    
    def get_display_price(self):
        return self.price / 100
    

class FeaturedProduct(models.Model):
    product=models.ForeignKey(Product,related_name='featured_product',on_delete=models.CASCADE)
    def __str__(self):
        return self.product.title
    

class ProductReview(models.Model):
    product=models.ForeignKey(Product,related_name='review',on_delete=models.CASCADE)
    user=models.ForeignKey(User,related_name='product_review',on_delete=models.CASCADE)
    rating = models.SmallIntegerField(validators=[MaxValueValidator(5)])
    comment=models.CharField(max_length=200)

    def __str__(self):
        return self.user.username, self.product.title ,self.rating
