# Generated by Django 4.1.6 on 2023-02-04 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_photo',
            field=models.ImageField(default='default.jpeg', upload_to='profile_pics'),
        ),
    ]
