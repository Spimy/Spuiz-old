# Generated by Django 2.2.4 on 2020-05-15 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0018_auto_20200515_2218'),
    ]

    operations = [
        migrations.AddField(
            model_name='completedquiz',
            name='completed_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]