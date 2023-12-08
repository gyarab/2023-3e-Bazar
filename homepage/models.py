from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):  
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'

class Order(models.Model):
    Title = models.CharField(max_length=255)
    mail = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    description = models.TextField(blank = True, null = True)
    creator = models.ForeignKey(User, related_name='Orders', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='Orders', on_delete=models.CASCADE)

    def __str__(self):
        return self.Title
    
    class Meta:
        verbose_name_plural = 'Orders'


