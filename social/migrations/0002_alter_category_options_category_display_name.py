# Generated by Django 4.1.6 on 2023-02-04 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AddField(
            model_name='category',
            name='display_name',
            field=models.CharField(default='testing', max_length=100),
            preserve_default=False,
        ),
    ]