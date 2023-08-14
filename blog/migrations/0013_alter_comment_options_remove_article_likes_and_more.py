# Generated by Django 4.2.2 on 2023-08-10 11:30

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0012_article_likes'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-date'], 'verbose_name': 'نظر', 'verbose_name_plural': 'نظرات'},
        ),
        migrations.RemoveField(
            model_name='article',
            name='likes',
        ),
        migrations.AddField(
            model_name='comment',
            name='likes',
            field=models.ManyToManyField(related_name='likes', to=settings.AUTH_USER_MODEL, verbose_name='لایک'),
        ),
    ]
