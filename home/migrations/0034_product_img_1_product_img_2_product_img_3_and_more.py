# Generated by Django 4.2.2 on 2023-08-09 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0033_alter_product_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='img_1',
            field=models.ImageField(blank=True, null=True, upload_to='product_gallery', verbose_name='نصاویر گالری محصول'),
        ),
        migrations.AddField(
            model_name='product',
            name='img_2',
            field=models.ImageField(blank=True, null=True, upload_to='product_gallery', verbose_name='نصاویر گالری محصول'),
        ),
        migrations.AddField(
            model_name='product',
            name='img_3',
            field=models.ImageField(blank=True, null=True, upload_to='product_gallery', verbose_name='نصاویر گالری محصول'),
        ),
        migrations.AddField(
            model_name='product',
            name='img_4',
            field=models.ImageField(blank=True, null=True, upload_to='product_gallery', verbose_name='نصاویر گالری محصول'),
        ),
    ]
