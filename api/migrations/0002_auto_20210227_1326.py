# Generated by Django 3.0.5 on 2021-02-27 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='titles',
            name='year',
            field=models.DateField(auto_now_add=True, verbose_name='Дата публикации'),
        ),
    ]
