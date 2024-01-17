from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from datetime import datetime
from django.contrib.auth import get_user_model

User = get_user_model()

class Listing(models.Model):
    class SaleType(models.TextChoices):
        FOR_SALE = 'for_sale'
        FOR_RENT = 'for_rent'

    realtor = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    bedrooms = models.IntegerField()
    bathrooms = models.DecimalField(max_digits=2, decimal_places=1)
    sale_type = models.CharField(max_length=10, choices=SaleType.choices, default=SaleType.FOR_SALE)
    photo_main = models.ImageField(upload_to='listing_imgs/%Y/%m/%d')
    photo_1 = models.ImageField(upload_to='listing_imgs/%Y/%m/%d', blank=True)
    photo_2 = models.ImageField(upload_to='listing_imgs/%Y/%m/%d', blank=True)
    photo_3 = models.ImageField(upload_to='listing_imgs/%Y/%m/%d', blank=True)
    is_published = models.BooleanField(default=True)
    listing_date = models.DateTimeField(default=timezone.now, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title