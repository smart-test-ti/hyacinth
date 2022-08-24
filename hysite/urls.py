# -*- coding:utf-8 -*-
from django.urls import path
from hysite.views import login

app_name = 'hysite'

urlpatterns = [
    path('',login.Login.loginPage, name='loginPage'),
    path('login/signin', login.Login.loginPage, name='loginPage'),
    path('login/api/signin', login.Login._api_signIn, name='_api_signIn '),
    path('login/api/logout', login.Login._api_logOut, name='_api_logOut'),
    path('db/choose', login.DB.dbChoosePage, name='dbChoosePage'),
    path('db/config', login.DB.dbConfigPage, name='dbConfigPage'),
    path('db/result', login.DB.dbResultPage, name='dbResultPage'),

]