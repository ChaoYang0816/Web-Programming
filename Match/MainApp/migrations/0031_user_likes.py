# Generated by Django 2.1.2 on 2018-11-28 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0030_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='likes',
            field=models.ManyToManyField(to='MainApp.Like'),
        ),
    ]
