# Generated by Django 4.2.2 on 2023-07-15 14:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0023_rename_prodcut_chart_product'),
        ('cart', '0004_alter_cart_variant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='variant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.variants', verbose_name='انتخاب گونه محصول'),
        ),
    ]
