# Generated by Django 4.2.2 on 2023-07-19 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0031_gallery_sale_off_gallery_sale_session_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='brand/', verbose_name='تصویر برند '),
        ),
    ]
