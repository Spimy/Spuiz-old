# Generated by Django 2.2.4 on 2020-04-27 13:41

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=255)),
                ('correct', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), blank=True, size=None)),
                ('wrong', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), blank=True, size=None)),
                ('thumbnail', models.ImageField(upload_to='Question_Thumbnails')),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('media_quiz', models.BooleanField(default=False)),
                ('mcq', models.BooleanField(default=False)),
                ('questions', models.ManyToManyField(to='Main.Question')),
            ],
            options={
                'verbose_name_plural': 'Quizzes',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(null=True, upload_to='User_Avatars')),
                ('quizzes', models.ManyToManyField(to='Main.Quiz')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
