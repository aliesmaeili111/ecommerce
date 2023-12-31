# Generated by Django 4.2.2 on 2023-07-16 07:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0024_alter_variants_change_alter_variants_update'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='num_view',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='view',
            field=models.ManyToManyField(blank=True, null=True, related_name='product_view', to=settings.AUTH_USER_MODEL),
        ),
    ]
