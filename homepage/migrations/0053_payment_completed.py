# Generated by Django 4.2.5 on 2024-03-03 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0052_remove_payment_code_payment_cid'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
