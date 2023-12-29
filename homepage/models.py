from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

class Category(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):  
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'

class Order(models.Model):
    Title = models.CharField(max_length=255)
    mail = models.CharField(max_length=255)
    price = models.IntegerField()
    phone_number = models.CharField(max_length=255)
    description = models.TextField(blank = True, null = True)
    creation_date = models.DateTimeField(default=now)
    expired = models.BooleanField(default=False)
    creator = models.ForeignKey(User, related_name='Orders', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='Orders', on_delete=models.CASCADE)

    def __str__(self):
        return self.Title
        
    class Meta:
        verbose_name_plural = 'Orders'

class OrderAttachment(models.Model):
    picture1 = models.ImageField(upload_to='images/', default='images/sedan.png')
    picture2 = models.ImageField(upload_to='images/', default='images/sedan.png')
    picture3 = models.ImageField(upload_to='images/', default='images/sedan.png')
    picture4 = models.ImageField(upload_to='images/', default='images/sedan.png')
    order = models.ForeignKey(Order, related_name='attachment',on_delete=models.CASCADE)

    def __str__(self):
        return self.order.Title
    
    class Meta:
        verbose_name_plural = 'OrderAttachments'

class Theme(models.Model):
    theme = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name='Themes', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username