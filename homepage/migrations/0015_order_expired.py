# Generated by Django 5.0 on 2023-12-26 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0014_remove_order_expired'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='expired',
            field=models.BooleanField(default=False),
        ),
    ]
