# Generated by Django 5.0 on 2023-12-30 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0017_alter_theme_options_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='rating',
            field=models.IntegerField(default=0),
        ),
    ]
