from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now
from ckeditor.fields import RichTextField


class Category(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Order(models.Model):
    Title = models.CharField(max_length=255)
    mail = models.CharField(max_length=255)
    price = models.IntegerField()
    phone_number = models.CharField(max_length=255)
    description = RichTextField(blank=True, null=True)
    creation_date = models.DateTimeField(default=now)
    expired = models.BooleanField(default=False)
    creator = models.ForeignKey(User, related_name="Orders", on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, related_name="Orders", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.Title

    class Meta:
        verbose_name_plural = "Orders"


class Theme(models.Model):
    theme = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="Themes", on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "Themes"


class User_attachments(models.Model):
    rating = models.IntegerField(default=0)
    Country = models.CharField(max_length=255, default="")
    City = models.CharField(max_length=255, default="")
    Street = models.CharField(max_length=255, default="")
    Postal_code = models.CharField(max_length=255, default="")
    user = models.ForeignKey(
        User, related_name="User_attachments", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "User_attachments"


class Rating_Relation(models.Model):
    rating_subject = models.ForeignKey(
        User, related_name="Rating_Subjects", on_delete=models.CASCADE
    )
    rating_creator = models.ForeignKey(
        User, related_name="Rating_Creators", on_delete=models.CASCADE
    )
    comment = models.TextField(default="")

    def __str__(self):
        return (
            self.rating_subject.username + " hodnotil " + self.rating_creator.username
        )
