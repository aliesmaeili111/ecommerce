# Generated by Django 4.2.2 on 2023-07-08 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20230628_1241'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, default='user.png', null=True, upload_to='profile/'),
        ),
    ]
