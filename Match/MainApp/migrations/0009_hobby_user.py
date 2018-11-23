# Generated by Django 2.1.2 on 2018-11-11 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('MainApp', '0008_auto_20181111_1853'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hobby',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hobbyName', models.CharField(max_length=10)),
                ('hobbyInfo', models.TextField(max_length=3000)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=10)),
                ('lastName', models.CharField(max_length=10)),
                ('age', models.IntegerField()),
                ('dob', models.DateField()),
                ('gender', models.CharField(max_length=8)),
                ('email', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
                ('profilePic', models.ImageField(upload_to='profile_images')),
                ('hobbies', models.ManyToManyField(to='MainApp.Hobby')),
            ],
        ),
    ]
