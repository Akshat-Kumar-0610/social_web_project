# Generated by Django 3.1.4 on 2021-01-16 20:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210111_1607'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='s_ban',
        ),
    ]
