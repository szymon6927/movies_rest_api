# Generated by Django 2.2.1 on 2019-05-11 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_auto_20190511_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='title',
            field=models.CharField(max_length=150, null=True, unique=True),
        ),
    ]
