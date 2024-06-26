# Generated by Django 5.0.2 on 2024-03-18 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('myapp', '0003_user_delete_customuser'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='birth_date',
            new_name='birthdate',
        ),
        migrations.AlterField(
            model_name='user',
            name='city',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, related_name='customuser_groups', to='auth.group'),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, related_name='customuser_permissions', to='auth.permission'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
