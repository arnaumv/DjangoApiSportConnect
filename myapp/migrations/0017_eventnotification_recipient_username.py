# Generated by Django 3.2 on 2024-05-09 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0016_auto_20240509_1314'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventnotification',
            name='recipient_username',
            field=models.CharField(default='default_username', max_length=255),
        ),
    ]
