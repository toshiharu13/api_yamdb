# Generated by Django 3.0.5 on 2021-02-19 06:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authorize', '0002_auto_20210219_0629'),
    ]

    operations = [
        migrations.RenameField(
            model_name='preuser',
            old_name='code',
            new_name='confirmation_code',
        ),
    ]
