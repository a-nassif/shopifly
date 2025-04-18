# Generated by Django 5.2 on 2025-04-18 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='theme',
            field=models.CharField(default='theme_1', max_length=255),
        ),
        migrations.AlterField(
            model_name='store',
            name='currency',
            field=models.CharField(choices=[('IQD', 'IQD - Iraqi Dinar'), ('JOD', 'JOD - Jordanian Dinar'), ('USD', 'USD - US Dollar'), ('EUR', 'EUR - Euro'), ('GBP', 'GBP - Great British Pound')], default='IQD', max_length=10),
        ),
        migrations.AlterField(
            model_name='store',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='store_logos'),
        ),
    ]
