# Generated by Django 3.0.5 on 2021-02-28 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='title',
            name='rating',
            field=models.FloatField(null=True),
        ),
    ]
