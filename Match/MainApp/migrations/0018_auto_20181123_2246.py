# Generated by Django 2.1.2 on 2018-11-23 22:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0017_hobby_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='hobbies',
        ),
        migrations.DeleteModel(
            name='Hobby',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
