# Generated by Django 5.2 on 2025-04-18 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_store_theme_alter_store_currency_alter_store_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.TextField(default='-'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(default='-', upload_to='product_images'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='stock',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
