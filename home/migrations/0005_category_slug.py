# Generated by Django 4.2.2 on 2023-06-30 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_remove_product_total_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(allow_unicode=True, blank=True, null=True, unique=True),
        ),
    ]
