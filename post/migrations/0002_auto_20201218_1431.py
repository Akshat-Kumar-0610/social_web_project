# Generated by Django 3.1.4 on 2020-12-18 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='name',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
