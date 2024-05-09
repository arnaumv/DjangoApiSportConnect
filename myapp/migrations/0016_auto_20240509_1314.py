# Generated by Django 3.2 on 2024-05-09 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0015_notification'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('follow', 'Follow'), ('create', 'Create'), ('join', 'Join')], max_length=6)),
                ('username', models.CharField(max_length=255)),
                ('event_title', models.CharField(blank=True, max_length=255)),
                ('event_sport', models.CharField(blank=True, max_length=255)),
                ('event_location', models.CharField(blank=True, max_length=255)),
                ('event_date', models.DateTimeField(blank=True, null=True)),
                ('event_time', models.TimeField(blank=True, null=True)),
                ('message', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Notification',
        ),
    ]
