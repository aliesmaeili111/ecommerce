# Generated by Django 4.2.2 on 2023-07-15 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_alter_coupon_options_alter_itemorder_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='code',
            field=models.CharField(blank=True, max_length=300, verbose_name='کد سفارش'),
        ),
    ]