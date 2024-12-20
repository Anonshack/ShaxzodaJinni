# Generated by Django 4.2.16 on 2024-11-16 10:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ContactMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(blank=True, max_length=20)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Internship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='internships/')),
                ('title', models.CharField(max_length=255)),
                ('published', models.DateField(blank=True, null=True)),
                ('description', models.TextField()),
                ('full_description', models.TextField()),
                ('apply_url', models.URLField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='InternshipCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='InternshipApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(max_length=255, upload_to='apply/')),
                ('title_1', models.CharField(max_length=255)),
                ('title_2', models.CharField(max_length=255)),
                ('title_3', models.CharField(max_length=255)),
                ('title_4', models.CharField(max_length=255)),
                ('applied_at', models.DateTimeField(auto_now_add=True)),
                ('internship', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.internship')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='internship',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.internshipcategory'),
        ),
        migrations.AddField(
            model_name='internship',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.company'),
        ),
        migrations.AddField(
            model_name='internship',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='internship_applications', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('pending', 'Ko‘rib chiqilmoqda'), ('approved', 'Tasdiqlangan'), ('rejected', 'Rad etilgan')], default='pending', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
