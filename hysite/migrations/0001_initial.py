# Generated by Django 4.1.6 on 2023-02-10 01:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='package_info',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('pkgname', models.CharField(max_length=64)),
                ('platform', models.CharField(default='Android', max_length=64)),
                ('key', models.TextField(null=True)),
                ('icon', models.TextField(null=True)),
                ('creater', models.TextField(default='hyacinth')),
                ('newest_version', models.TextField(null=True)),
                ('ctime', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='package_list',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('build_num', models.IntegerField(default=0)),
                ('pkgname', models.CharField(max_length=64)),
                ('version', models.CharField(max_length=64)),
                ('platform', models.CharField(max_length=64)),
                ('filename', models.CharField(max_length=64)),
                ('filepath', models.TextField(default='')),
                ('is_share', models.IntegerField(default=0)),
                ('ctime', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
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
        migrations.CreateModel(
            name='package_share_info',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('token', models.CharField(max_length=64)),
                ('pkgname', models.CharField(max_length=64)),
                ('version', models.CharField(max_length=64)),
                ('platform', models.CharField(max_length=64)),
                ('filename', models.CharField(max_length=64)),
                ('filepath', models.TextField(default='')),
                ('ctime', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='package_version_list',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('pkgname', models.CharField(max_length=64)),
                ('version', models.CharField(max_length=64)),
                ('ctime', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='platform',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('is_show_admin', models.BooleanField(default=False)),
                ('db_type', models.TextField(default='SQLite', max_length=64)),
                ('db_status', models.BooleanField(default=True)),
                ('db_name', models.TextField(max_length=64, null=True)),
                ('db_host', models.TextField(max_length=64, null=True)),
                ('db_port', models.TextField(max_length=64, null=True)),
                ('db_user', models.TextField(max_length=64, null=True)),
                ('db_password', models.TextField(max_length=64, null=True)),
                ('ctime', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=64)),
                ('password', models.CharField(max_length=64)),
                ('nickname', models.CharField(max_length=64)),
                ('avatar', models.TextField(null=True)),
                ('role', models.TextField(default='普通用户')),
                ('mobile', models.TextField(null=True)),
                ('email', models.TextField(null=True)),
                ('token', models.TextField(null=True)),
                ('initialized', models.IntegerField(default=0)),
                ('ctime', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
