# Generated by Django 2.1.2 on 2018-11-27 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0024_auto_20181127_1203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profilePic',
            field=models.ImageField(blank=True, default='/static/MainApp/profile-image.jpg', upload_to='profile_images'),
        ),
    ]
