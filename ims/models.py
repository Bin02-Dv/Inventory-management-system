from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

# Create your models here.


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    profileimg = models.ImageField(upload_to='profileImg', default='user.png')
    full_name = models.CharField(max_length=100, blank=True)
    user_address = models.TextField(max_length=100, blank=True)
    user_phone = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username

class Stock(models.Model):
    category = models.CharField(max_length=100, blank=True)
    product_name = models.CharField(max_length=100, blank=True)
    product_qtn = models.IntegerField(blank=True)
    price = models.IntegerField(blank=True)
    sale_price = models.IntegerField(blank=True)
    expiry_date = models.CharField(blank=True)
    manufacturer_date = models.CharField(blank=True)
    date = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.product_name

class Category(models.Model):
    category = models.CharField(max_length=100, blank=True)
    date = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.category
    
class Sales(models.Model):
    user = models.CharField(max_length=100, blank=True)
    client_name = models.CharField(max_length=100, blank=True)
    client_phone = models.CharField(max_length=100, blank=True)
    client_address = models.CharField(max_length=100, blank=True)
    products = models.CharField(max_length=100, blank=True)
    total_qtn = models.IntegerField(blank=True)
    total_price = models.IntegerField(blank=True)
    date = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.products

class History(models.Model):
    user = models.CharField(max_length=100, blank=True)
    client_name = models.CharField(max_length=100, blank=True)
    client_phone = models.CharField(max_length=100, blank=True)
    client_address = models.CharField(max_length=100, blank=True)
    products = models.CharField(max_length=100, blank=True)
    total_qtn = models.IntegerField(blank=True)
    total_price = models.IntegerField(blank=True)
    date = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.products
    
class Transaction(models.Model):
    transactions = models.CharField(max_length=100, blank=True)
    date = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.transactions



