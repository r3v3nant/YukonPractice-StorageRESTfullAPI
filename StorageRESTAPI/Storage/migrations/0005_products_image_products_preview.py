# Generated by Django 5.1.6 on 2025-02-26 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Storage', '0004_alter_products_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='image',
            field=models.ImageField(null=True, upload_to='products/'),
        ),
        migrations.AddField(
            model_name='products',
            name='preview',
            field=models.ImageField(blank=True, null=True, upload_to='products/previews/'),
        ),
    ]
