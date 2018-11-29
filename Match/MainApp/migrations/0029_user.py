# Generated by Django 2.1.2 on 2018-11-29 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0028_auto_20181129_1057'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('firstName', models.CharField(max_length=20)),
                ('lastName', models.CharField(max_length=20)),
                ('age', models.IntegerField()),
                ('dob', models.DateField()),
                ('gender', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=50, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=50)),
                ('profilePic', models.ImageField(blank=True, upload_to='profile_images')),
                ('hobbies', models.ManyToManyField(to='MainApp.Hobby')),
            ],
        ),
    ]
