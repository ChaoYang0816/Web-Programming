# Generated by Django 2.1.2 on 2018-11-24 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0021_hobby_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profilePic',
            field=models.ImageField(upload_to=''),
        ),
    ]
