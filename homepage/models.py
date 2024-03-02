from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now
from ckeditor_uploader.fields import RichTextUploadingField

# category model
class Category(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

# Order model 
class Order(models.Model):
    Title = models.CharField(max_length=255)
    price = models.IntegerField()
    description = RichTextUploadingField(blank=True, null=True)
    creation_date = models.DateTimeField(default=now)
    expired = models.BooleanField(default=False)
    creator = models.ForeignKey(User, related_name="Orders", on_delete=models.CASCADE)
    importance = models.IntegerField(default=0)
    # every category has its orders
    category = models.ForeignKey(
        Category, related_name="Orders", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.Title

    class Meta:
        verbose_name_plural = "Orders"

# attachments to the user model
class User_attachments(models.Model):
    rating = models.IntegerField(default=0)
    City = models.CharField(max_length=255, default="")
    Street = models.CharField(max_length=255, default="")
    Postal_code = models.CharField(max_length=255, default="")
    phone_number = models.CharField(max_length=255, default="")
    theme = models.CharField(max_length=255, default="")
    # every on of those has its user
    user = models.ForeignKey(
        User, related_name="User_attachments", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "User_attachments"

# is used so you can rate a user just one time
class Rating_Relation(models.Model):
    # rated user
    rating_subject = models.ForeignKey(
        User, related_name="Rating_Subjects", on_delete=models.CASCADE
    )
    # user rating
    rating_creator = models.ForeignKey(
        User, related_name="Rating_Creators", on_delete=models.CASCADE
    )
    # rating user comment
    comment = models.TextField(default="")

    def __str__(self):
        return (
            self.rating_subject.username + " hodnotil " + self.rating_creator.username
        )

# chat model
class chat(models.Model):
    # 1 user of the conversation
    user_1 = models.ForeignKey(User, related_name="User_1", on_delete=models.CASCADE)
    # 2 user of the conversation
    user_2 = models.ForeignKey(User, related_name="User_2", on_delete=models.CASCADE) 
    # the id of the order that the chat is about
    order_id = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Chats"

    def __str__(self):
        return (
            self.user_1.username
            + " chat with "
            + self.user_2.username
            + " about "
            + str(self.order_id)
        )

# message model 
class message(models.Model):
    # chat that the message is in
    chat = models.ForeignKey(chat, related_name="Chat", on_delete=models.CASCADE)
    # user that sent the message
    message_sender = models.ForeignKey(
        User, related_name="Message_Sender", on_delete=models.CASCADE
    )
    # the actual text of the message
    message = models.TextField()
    # date when the message was sent
    creation_date = models.DateTimeField(default=now)

    class Meta:
        verbose_name_plural = "Messages"

    def __str__(self):
        return self.message_sender.username + " message"
