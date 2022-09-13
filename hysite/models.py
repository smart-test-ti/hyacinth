from django.db import models
from django.utils import timezone

# Create your models here.

class platform(models.Model):
    """platform info table"""
    id = models.AutoField(primary_key=True)
    is_show_admin = models.BooleanField(default=False)
    db_type = models.TextField(max_length=64, default='SQLite')
    db_status = models.BooleanField(default=True)
    db_name = models.TextField(max_length=64, null=True)
    db_host = models.TextField(max_length=64, null=True)
    db_port = models.TextField(max_length=64, null=True)
    db_user = models.TextField(max_length=64, null=True)
    db_password = models.TextField(max_length=64, null=True)
    ctime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return ' %s' % ( self.db_type)

class user(models.Model):
    """user info table"""
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    nickname = models.CharField(max_length=64)
    avatar = models.TextField(null=True)
    role = models.TextField(default='普通用户')
    mobile = models.TextField(null=True)
    email = models.TextField(null=True)
    token = models.TextField(null=True)
    initialized = models.IntegerField(default=0)
    ctime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return ' %s' % ( self.username)



class package_info(models.Model):
    """package info table"""
    id = models.AutoField(primary_key=True)
    pkgname = models.CharField(max_length=64)
    platform = models.CharField(max_length=64, default='Android')
    key = models.TextField(null=True)
    icon = models.TextField(null=True)
    newest_version = models.TextField(null=True)
    ctime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return ' %s' % ( self.pkgname)

class package_list(models.Model):
    """package list table"""
    id = models.AutoField(primary_key=True)
    pkgname = models.CharField(max_length=64)
    version = models.CharField(max_length=64)
    platform = models.CharField(max_length=64)
    filename = models.CharField(max_length=64)
    is_share = models.IntegerField(default=0)
    ctime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return ' %s' % ( self.pkgname)