# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.contrib import auth
from django.http import HttpResponse
import json
import time
import requests
import sys
from hysite import models
from hysite.public.common import Method
from hysite.public.decorators import Decorators
sys.getdefaultencoding()

common = Method()

class User:

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def userPage(cls, request, *arg, **kwargs):
        page = int(kwargs['page'])
        nickname = request.session['nickname']
        users = models.user.objects.all().order_by('-id')
        # apks = models.package.objects.all().order_by('-id')
        # apk_num = models.package.objects.all().count()
        # paginator = Paginator(apks, 2)
        # page_obj = paginator.get_page(page)
        return render(request, 'user.html', locals())

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def createUserAPI(cls, request):
        username = common._request(request, 'username')
        nickname = common._request(request, 'nickname')
        password = common._request(request, 'password')
        ctime  = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        user = models.user.objects.filter(username=username)
        if user:
            result = {'status': 0, 'msg': 'user existed'}
        else:
            models.user(username=username, password=password, nickname=nickname, ctime=ctime).save()
            result = {'status': 1, 'msg': 'create user success'}
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def editUserAPI(cls, request):
        username = common._request(request, 'username')
        nickname = common._request(request, 'nickname')
        password = common._request(request, 'password')
        role = common._request(request, 'role')
        try:
            models.user.objects.filter(username=username).update(nickname=nickname, password=password, role=role)
            result = {'status': 1, 'msg': 'edit user success'}
        except Exception as e:
            result = {'status': 0, 'msg': str(e)}

        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def deleteUserAPI(cls, request):
        session_name = request.session['username']
        username = common._request(request, 'username')
        if session_name != username:
            try:
                models.user.objects.filter(username=username).delete()
                result = {'status': 1, 'msg': 'delete user success'}
            except Exception as e:
                result = {'status': 0, 'msg': str(e)}
        else:
            result = {'status': 0, 'msg': 'you can not delete yourself'}
        return HttpResponse(json.dumps(result), content_type="application/json")


