# Generated by Django 3.0.4 on 2020-03-19 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0002_auto_20200319_0224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
