# Generated by Django 2.2.4 on 2020-04-27 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0007_auto_20200427_2019'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='thumbnail',
            field=models.ImageField(default=1, upload_to='Quiz_Thumbnails'),
            preserve_default=False,
        ),
    ]
