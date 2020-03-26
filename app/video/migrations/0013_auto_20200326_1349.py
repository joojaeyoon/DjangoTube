# Generated by Django 3.0.4 on 2020-03-26 04:49

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('video', '0012_auto_20200326_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='subscribed',
            field=models.ManyToManyField(blank=True, related_name='subscriber_list', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='profile',
            name='subscriber',
            field=models.ManyToManyField(blank=True, related_name='subscribed_list', to=settings.AUTH_USER_MODEL),
        ),
    ]
