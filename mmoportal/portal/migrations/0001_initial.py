# Generated by Django 4.2.9 on 2024-01-17 20:10

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
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Танк', 'Танк'), ('Хилер', 'Хилер'), ('ДД', 'ДД'), ('Гилдмастер', 'Гилдмастер'), ('Квестгивер', 'Квестгивер'), ('Кузнец', 'Кузнец'), ('Кожевник', 'Кожевник'), ('Зельевар', 'Зельевар'), ('Мастер заклинаний', 'Мастер заклинаний')], default='tank', max_length=18)),
                ('subscribers', models.ManyToManyField(blank=True, related_name='categories', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Название', max_length=256)),
                ('text', models.CharField(max_length=256)),
                ('time_created', models.DateTimeField(auto_now_add=True, verbose_name='Время')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal.author')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal.categories')),
            ],
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=256)),
                ('date_create', models.DateTimeField(auto_now_add=True, verbose_name='Время')),
                ('validated', models.BooleanField(default=False)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replied', to='portal.post')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
