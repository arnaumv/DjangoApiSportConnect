# Generated by Django 5.0.2 on 2024-04-16 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_event_deleted_notify'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='image_path',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]