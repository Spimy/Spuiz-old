# Generated by Django 2.2.4 on 2020-04-27 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0009_auto_20200427_2127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='quizzes',
            field=models.ManyToManyField(blank=True, related_name='user_profile', to='Main.Quiz'),
        ),
    ]
