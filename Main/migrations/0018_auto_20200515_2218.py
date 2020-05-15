# Generated by Django 2.2.4 on 2020-05-15 18:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Main', '0017_userprofile_bio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='completed_quizzes',
        ),
        migrations.CreateModel(
            name='CompletedQuiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz', to='Main.Quiz')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Completed Quizzes',
            },
        ),
    ]
