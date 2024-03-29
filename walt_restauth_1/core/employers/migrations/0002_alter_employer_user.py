# Generated by Django 4.2.1 on 2023-06-19 00:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('employers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employer',
            name='user',
            field=models.ForeignKey(limit_choices_to={'roles': 'employer'}, on_delete=django.db.models.deletion.CASCADE, related_name='employer', to=settings.AUTH_USER_MODEL),
        ),
    ]
