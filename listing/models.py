from django.db import models
from django.utils.text import slugify
from uuid import uuid4
from django.utils import timezone
from datetime import datetime
from django.contrib.auth import get_user_model

class Banner(models.Model):
    name   = models.CharField(default='House',max_length=100)
    image = models.ImageField(upload_to='banner_imgs/')
    
    def __str__(self):
        return self.name
    
class PropertyType(models.Model):
    property_type   = models.CharField(default='House',max_length=100)
    image = models.ImageField(upload_to='property_type_imgs/')
    
    def __str__(self):
        return self.property_type

User = get_user_model()
class Listing(models.Model):
    class SaleType(models.TextChoices):
        FOR_SALE = 'for_sale'
        FOR_RENT = 'for_rent'

    realtor         = models.ForeignKey(User, on_delete=models.CASCADE)
    title           = models.CharField(max_length=200)
    slug            = models.SlugField(unique=True)
    address         = models.CharField(max_length=200)
    city            = models.CharField(max_length=100)
    state           = models.CharField(max_length=100)
    zipcode         = models.CharField(max_length=20)
    description     = models.TextField(blank=True)
    price           = models.IntegerField()
    bedrooms        = models.IntegerField()
    bathrooms       = models.DecimalField(max_digits=2, decimal_places=1)
    property_area   = models.IntegerField(default=0)
    property_type   = models.CharField(default='House',max_length=100)
    sale_type       = models.CharField(max_length=10, choices=SaleType.choices, default=SaleType.FOR_SALE)
    photo_main      = models.ImageField(upload_to='listing_imgs/')
    photo_1         = models.ImageField(upload_to='listing_imgs/', null=True, blank=True)
    photo_2         = models.ImageField(upload_to='listing_imgs/', null=True, blank=True)
    photo_3         = models.ImageField(upload_to='listing_imgs/', null=True, blank=True)
    is_published    = models.BooleanField(default=True)
    listing_date    = models.DateTimeField(default=timezone.now, blank=True)

    def save(self, *args, **kwargs):
        new_slug = slugify(self.title)
        if Listing.objects.filter(slug=new_slug).exists():
            new_slug = f"{new_slug}-{str(uuid4())[:8]}"
        self.slug = new_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title