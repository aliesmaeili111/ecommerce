# Generated by Django 4.2.2 on 2023-07-13 14:30

from django.db import migrations
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0021_variants_change'),
    ]

    operations = [
        migrations.AddField(
            model_name='variants',
            name='update',
            field=django_jalali.db.models.jDateTimeField(auto_now=True),
        ),
    ]
