# Generated by Django 3.0.5 on 2021-02-27 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20210227_1343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='titles',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Название пройзведения'),
        ),
    ]
