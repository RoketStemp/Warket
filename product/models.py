from io import BytesIO
from PIL import Image

from django.contrib.auth.models import User

from django.core.files import File
from django.core.validators import MaxValueValidator, MinValueValidator 

from django.db import models
from django.db.models.fields import related




DRIVE_TYPE_CHOICES = [
    ('HDD', 'HDD'),
    ('SSD', 'SSD')
]


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Category name')
    slug = models.SlugField()

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/{self.slug}/'
    

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.CharField(max_length=255)
    comment = models.ManyToManyField('self', related_name='subcomments')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    advantages = models.TextField(max_length=500, blank=True, null=True)
    disadvantages = models.TextField(max_length=500, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    is_reply = models.BooleanField(default=False)

    class Meta:
        ordering = ('-date_added',)

    def __str__(self):
        return self.text
    

class Product(models.Model):
    """Product model"""

    name = models.CharField(max_length=255, verbose_name='Product name')
    slug = models.SlugField()
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Product price')
    category = models.ForeignKey(Category, verbose_name='Category', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    comments = models.ManyToManyField(Comment, blank=True, null=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_added',)
        abstract = True

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}/'

    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000'+ self.image.url
        return ''

    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000'+ self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return 'http://127.0.0.1:8000'+ self.thumbnail.url
            else:
                return ''
    
    def make_thumbnail(self, image, size=(300,200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail
    

class Laptops(Product):
    screen_resolution = models.CharField(max_length=255, verbose_name='Screen resolution')
    screen_type = models.CharField(max_length=255, verbose_name='Screen type')
    processor = models.CharField(max_length=255, verbose_name='Processor')
    ram = models.CharField(max_length=255, verbose_name='RAM')
    drive_type = models.CharField(max_length=50, choices=DRIVE_TYPE_CHOICES) 
    video = models.CharField(max_length=255, verbose_name='Video memory')
    battery = models.CharField(max_length=255, verbose_name='Battery amount')

    def __str__(self):
        return self.name


class Computers(Product):
    screen_resolution = models.CharField(max_length=255, verbose_name='Screen resolution')
    screen_type = models.CharField(max_length=255, verbose_name='Screen type')
    processor = models.CharField(max_length=255, verbose_name='Processor')
    ram = models.CharField(max_length=255, verbose_name='RAM')
    drive_type = models.CharField(max_length=50, choices=DRIVE_TYPE_CHOICES) 
    video = models.CharField(max_length=255, verbose_name='Video memory')

    def __str__(self):
        return self.name

