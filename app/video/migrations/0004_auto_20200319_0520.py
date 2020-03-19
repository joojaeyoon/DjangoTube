# Generated by Django 3.0.4 on 2020-03-19 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0003_auto_20200319_0253'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='view_count',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='video',
            name='video_link',
            field=models.FilePathField(path='/app/media/videos'),
        ),
    ]