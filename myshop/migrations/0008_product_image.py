# Generated by Django 3.0 on 2023-11-12 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myshop', '0007_auto_20231112_0608'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(default=None, upload_to=''),
        ),
    ]