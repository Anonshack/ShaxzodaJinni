# Generated by Django 4.2.16 on 2024-11-17 06:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='internship',
            name='user',
        ),
        migrations.RemoveField(
            model_name='internshipapplication',
            name='title_1',
        ),
        migrations.RemoveField(
            model_name='internshipapplication',
            name='title_2',
        ),
        migrations.RemoveField(
            model_name='internshipapplication',
            name='title_3',
        ),
        migrations.RemoveField(
            model_name='internshipapplication',
            name='title_4',
        ),
        migrations.AddField(
            model_name='internshipapplication',
            name='additional_titles',
            field=models.JSONField(default=dict),
        ),
        migrations.AddField(
            model_name='internshipapplication',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='internshipapplication',
            name='status',
            field=models.CharField(choices=[('pending', 'Ko‘rib chiqilmoqda'), ('approved', 'Tasdiqlangan'), ('rejected', 'Rad etilgan')], default='pending', max_length=10),
        ),
        migrations.AlterField(
            model_name='internshipapplication',
            name='internship',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='main_app.internship'),
        ),
        migrations.AlterField(
            model_name='internshipapplication',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Application',
        ),
    ]
