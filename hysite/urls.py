# -*- coding:utf-8 -*-
from django.urls import path
from hysite.views import login, package, user


app_name = 'hysite'

urlpatterns = [

    # Login
    path('',login.Initialize.initializeResultPage, name='initializeResultPage'),
    path('login/signin', login.Login.loginPage, name='loginPage'),
    path('login/api/signin', login.Login.signinAPI, name='signinAPI '),
    path('login/api/signup', login.Login.signupAPI, name='signupAPI '),
    path('login/api/logout', login.Login.logoutAPI, name='logoutAPI'),
    path('initialize/db/choose', login.Initialize.dbChoosePage, name='dbChoosePage'),
    path('initialize/db/config', login.Initialize.dbConfigPage, name='dbConfigPage'),
    path('initialize/result', login.Initialize.initializeResultPage, name='initializeResultPage'),

    # package
    path('package/home/app=<app>', package.Home.packageInfoPage, name='packageInfoPage'),
    path('package/manage', package.Manage.packageManagePage, name='packageManagePage'),
    path('package/list/app=<app>&version=<version>', package.List.packageListPage, name='packageListPage'),

    path('package/api/get', package.Home.getPackageAPI, name='getPackageAPI'),
    path('package/api/create', package.Home.createPackageAPI, name='createPackageAPI'),
    path('package/api/delete', package.Home.deletePackageAPI, name='deletePackageAPI'),
    path('package/api/upload/logo', package.Home.uploadLogoAPI, name='uploadLogoAPI'),

    path('package/api/version', package.List.getPackageVersionAPI, name='getPackageVersionAPI'),
    path('package/api/file/create', package.List.createVersionFileAPI, name='createVersionFileAPI'),
    path('package/api/file/delete', package.List.deleteVersionFileAPI, name='deleteVersionFileAPI'),

    # user
    path('user/list', user.User.userPage, name='userPage'),
    path('user/api/create', user.User.createUserAPI, name='createUserAPI'),
    path('user/api/info', user.User.getUserAPI, name='getUserAPI'),
    path('user/api/edit', user.User.editUserAPI, name='editUserAPI'),
    path('user/api/delete', user.User.deleteUserAPI, name='deleteUserAPI'),
    path('user/setting', user.Setting.settingPage, name='settingPage'),

]