# Generated by Django 5.0 on 2023-12-16 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='picture1',
        ),
        migrations.RemoveField(
            model_name='order',
            name='picture2',
        ),
        migrations.RemoveField(
            model_name='order',
            name='picture3',
        ),
        migrations.RemoveField(
            model_name='order',
            name='picture4',
        ),
        migrations.AddField(
            model_name='order',
            name='pictures',
            field=models.FileField(default='circuit.png', upload_to='images/'),
        ),
    ]
