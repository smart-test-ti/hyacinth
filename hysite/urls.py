# -*- coding:utf-8 -*-
from django.urls import path
from hysite.views import login, package, user


app_name = 'hysite'

urlpatterns = [
    path('',login.Initialize.initializeResultPage, name='initializeResultPage'),
    path('login/signin', login.Login.loginPage, name='loginPage'),
    path('login/api/signin', login.Login.signinAPI, name='signinAPI '),
    path('login/api/signup', login.Login.signupAPI, name='signupAPI '),
    path('login/api/logout', login.Login.logoutAPI, name='logoutAPI'),
    path('initialize/db/choose', login.Initialize.dbChoosePage, name='dbChoosePage'),
    path('initialize/db/config', login.Initialize.dbConfigPage, name='dbConfigPage'),
    path('initialize/result', login.Initialize.initializeResultPage, name='initializeResultPage'),

    # package
    path('package/home/page=<page>', package.Manage.packageInfoPage, name='packageInfoPage'),
    path('package/list/package=<package>&version=<version>', package.Manage.packageListPage, name='packageListPage'),

    # user
    path('user/list/page=<page>', user.User.userPage, name='userPage'),
    path('user/api/create', user.User.createUserAPI, name='createUserAPI'),
    path('user/api/info', user.User.getUserAPI, name='getUserAPI'),
    path('user/api/edit', user.User.editUserAPI, name='editUserAPI'),
    path('user/api/delete', user.User.deleteUserAPI, name='deleteUserAPI'),

]