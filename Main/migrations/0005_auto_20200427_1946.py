# Generated by Django 2.2.4 on 2020-04-27 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0004_auto_20200427_1939'),
    ]

    operations = [
        migrations.CreateModel(
            name='CorrectAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='WrongAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='question',
            name='correct',
        ),
        migrations.RemoveField(
            model_name='question',
            name='wrong',
        ),
        migrations.AddField(
            model_name='question',
            name='correct',
            field=models.ManyToManyField(to='Main.CorrectAnswer'),
        ),
        migrations.AddField(
            model_name='question',
            name='wrong',
            field=models.ManyToManyField(blank=True, to='Main.WrongAnswer'),
        ),
    ]
