# Generated by Django 2.2.4 on 2020-04-27 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0006_auto_20200427_2015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, null=True),
        ),
    ]
