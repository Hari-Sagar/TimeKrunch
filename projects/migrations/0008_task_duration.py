# Generated by Django 5.0.6 on 2024-10-20 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_task_featured_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='duration',
            field=models.IntegerField(default=1),
        ),
    ]
