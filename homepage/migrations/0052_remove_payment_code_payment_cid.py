# Generated by Django 4.2.5 on 2024-03-03 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0051_payment_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='code',
        ),
        migrations.AddField(
            model_name='payment',
            name='cid',
            field=models.CharField(default='', max_length=255),
        ),
    ]
