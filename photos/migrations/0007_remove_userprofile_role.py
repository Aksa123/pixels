# Generated by Django 3.0 on 2020-06-24 01:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0006_auto_20200624_0842'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='role',
        ),
    ]
