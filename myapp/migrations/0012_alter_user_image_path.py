# Generated by Django 4.2 on 2024-04-17 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_user_image_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image_path',
            field=models.ImageField(default='User_photo.png', upload_to='profile_photos'),
        ),
    ]
