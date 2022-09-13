# -*- coding:utf-8 -*-
from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib import auth
from django.http import HttpResponse
import json
import requests
import sys
from hysite import models
from hysite.public.common import Method
from hysite.public.decorators import Decorators
sys.getdefaultencoding()

common = Method()

class Login(View):

    @classmethod
    def loginPage(cls, request):
        """登陆页面"""
        count = models.user.objects.filter(username='hyacinth', password='CjOQ2ME7Rilash66').count()
        if count == 0:
            return redirect('/initialize/result')
        return render(request, 'sign-in.html', locals())


    @classmethod
    @method_decorator(Decorators.catch_except)
    def signinAPI(cls, request):
        """登录接口"""
        username = common._request(request, 'username')
        password = common._request(request, 'password')
        user = models.user.objects.filter(username=username, password=password)
        if user:
            request.session['is_login'] = '1'
            request.session['username'] = username
            nickname = models.user.objects.filter(username=username).values("nickname").first()['nickname']
            request.session['nickname'] = nickname
            result = {'status': 1, 'msg': 'login success'}
        else:
            result = {'status': 0, 'msg': 'the password is incorrect'}
        return HttpResponse(json.dumps(result), content_type="application/json")


    @classmethod
    @method_decorator(Decorators.catch_except)
    def signupAPI(cls, request):
        """注册接口"""
        username = common._request(request, 'username')
        password = common._request(request, 'password')
        user = models.user.objects.filter(username=username, password=password)
        if user:
            result = {'status': 0, 'msg': 'user existed'}
        else:
            models.user(username=username, password=password, nickname=username).save()
            result = {'status': 1, 'msg': 'create user success'}
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    @method_decorator(Decorators.catch_except)
    def logoutAPI(cls, request):
        """退出登录接口"""
        auth.logout(request)
        request.session['is_login'] = '0'
        response = redirect('/login/signin')
        return response


class Initialize():

    @classmethod
    def dbChoosePage(cls, request):
        return render(request, 'db-choose.html', locals())

    @classmethod
    def dbConfigPage(cls, request):
        return render(request, 'db-config.html', locals())

    @classmethod
    def initializeResultPage(cls, request):
        """初始化结果页"""
        count = models.user.objects.filter(username='hyacinth', password='CjOQ2ME7Rilash66').count()
        if count > 0:
            initialized = models.user.objects.filter(username='hyacinth').values("initialized").last()['initialized']
            if initialized == 1:
                return redirect('/login/signin')
        else:
            models.user(username='hyacinth', password='CjOQ2ME7Rilash66', nickname='风信子', role='超级管理员').save()
        if request.path == '/':
            return redirect('/initialize/result')
        models.user.objects.filter(username='hyacinth').update(initialized=1)
        return render(request, 'db-result.html', locals())
