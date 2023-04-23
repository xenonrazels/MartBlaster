from django.db import models
from django.contrib.auth.models import User
from io import BytesIO
from PIL import Image
from django.core.files import File
import statistics

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
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    # vendor = models.ForeignKey(Vendor, related_name='products', on_delete=models.CASCADE)
    added_by=models.ForeignKey(User,related_name='products',on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)

    class Meta:
        ordering = ['-date_added']
    
    def __str__(self):
        return self.title
    
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

        return thumbnail