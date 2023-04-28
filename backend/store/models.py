from django.db import models
from django.contrib.auth.models import User
from io import BytesIO
from PIL import Image
from django.core.files import File
from django.contrib import messages 
from userProfile.models import Pasal


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
