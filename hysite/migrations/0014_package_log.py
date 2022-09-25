# Generated by Django 4.1.1 on 2022-09-25 14:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('hysite', '0013_delete_package_log'),
    ]

    operations = [
        migrations.CreateModel(
            name='package_log',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=64)),
                ('pkgname', models.TextField(null=True)),
                ('version', models.TextField(null=True)),
                ('filename', models.TextField(null=True)),
                ('action', models.TextField(null=True)),
                ('ctime', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
