# Generated by Django 3.2 on 2022-09-07 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hysite', '0006_package_info_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='package_info',
            name='platform',
            field=models.CharField(default='Android', max_length=64),
        ),
    ]
