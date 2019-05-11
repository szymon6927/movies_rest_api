# Generated by Django 2.2.1 on 2019-05-11 15:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_auto_20190510_1941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movierating',
            name='movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='movies.Movie'),
        ),
    ]
