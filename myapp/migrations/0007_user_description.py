# Generated by Django 4.2 on 2024-04-02 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_event_image_path_eventsjoined'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
