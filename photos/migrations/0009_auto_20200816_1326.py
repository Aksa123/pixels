# Generated by Django 3.0 on 2020-08-16 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0008_userprofile_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(default='default.jpg', upload_to='users'),
        ),
    ]