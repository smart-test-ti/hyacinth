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
        if request.path == '/':
            return redirect('/login/signin')
        return render(request, 'sign-in.html', locals())


    @classmethod
    @method_decorator(Decorators._catch_except)
    def _api_signIn(cls, request):
        """登录接口"""
        username = common.request_method(request, 'username')
        password = common.request_method(request, 'password')
        user = models.User.objects.filter(username=username, password=password)
        if user:
            request.session['is_login'] = '1'
            request.session['username'] = username
            nickname = models.User.objects.filter(username=username, password=password).values("nickname").first()[
                'nickname']
            request.session['nickname'] = nickname
            result = {'status': 1, 'msg': 'login success'}
        else:
            result = {'status': 0, 'msg': 'the password is incorrect'}
        return HttpResponse(json.dumps(result), content_type="application/json")


    @classmethod
    @method_decorator(Decorators._catch_except)
    def _api_signUp(cls, request):
        """注册接口"""
        username = common.request_method(request, 'username')
        password = common.request_method(request, 'password')
        user = models.User.objects.filter(username=username, password=password)
        if user:
            result = {'status': 0, 'msg': 'user existed'}
        else:
            models.User(username=username, password=password, nickname=username).save()
            result = {'status': 1, 'msg': 'create user success'}
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    @method_decorator(Decorators._catch_except)
    def _api_logOut(cls, request):
        """退出登录接口"""
        auth.logout(request)
        response = redirect('/login/signin')
        return response


class DB():

    @classmethod
    def dbChoosePage(cls, request):
        return render(request, 'db-choose.html', locals())

    @classmethod
    def dbConfigPage(cls, request):
        return render(request, 'db-config.html', locals())

    @classmethod
    def dbResultPage(cls, request):
        return render(request, 'db-result.html', locals())
