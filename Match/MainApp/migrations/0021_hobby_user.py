# Generated by Django 2.1.2 on 2018-11-24 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('MainApp', '0020_auto_20181124_1027'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hobby',
            fields=[
                ('hobbyName', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('hobbyInfo', models.TextField(max_length=3000)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=20)),
                ('lastName', models.CharField(max_length=20)),
                ('age', models.IntegerField()),
                ('dob', models.DateField()),
                ('gender', models.CharField(max_length=10)),
                ('email', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('profilePic', models.ImageField(upload_to='profile_images')),
                ('hobbies', models.ManyToManyField(to='MainApp.Hobby')),
            ],
        ),
    ]
