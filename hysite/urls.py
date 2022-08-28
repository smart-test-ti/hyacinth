# -*- coding:utf-8 -*-
from django.urls import path
from hysite.views import login, package


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
    path('package/manage/page=<page>', package.Manage.packageInfoPage, name='packageInfoPage'),
    path('package/list/page=<page>', package.Manage.packageListPage, name='packageListPage'),

]