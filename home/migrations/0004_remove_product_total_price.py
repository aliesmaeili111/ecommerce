# Generated by Django 4.2.2 on 2023-06-29 09:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_product_available_alter_product_amount_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='total_price',
        ),
    ]
