# Generated by Django 4.2.2 on 2023-06-30 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fun', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcement',
            name='comments',
            field=models.ManyToManyField(blank=True, related_name='commented_on', to='fun.comment'),
        ),
    ]
