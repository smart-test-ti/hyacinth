# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
import json
import sys
import re
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
        username = request.session['username']
        role = models.user.objects.filter(username=username).values("role").first()['role']
        users = models.user.objects.filter(~Q(role='超级管理员')).order_by('-id')
        # num = models.user.objects.all().count()
        # paginator = Paginator(users, 20)
        # page_obj = paginator.get_page(page)
        return render(request, 'user.html', locals())

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def getUserAPI(cls, request):
        username = common._request(request, 'username')
        try:
            users = models.user.objects.filter(username=username)
            data = [{'nickname': user.nickname, 'password': user.password,
                     'role': user.role, 'email': user.email, 'ctime': str(user.ctime)} for user in users]
            result = {'status': 1, 'data': data}
        except Exception as e:
            result = {'status': 0, 'msg': str(e)}
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def createUserAPI(cls, request):
        username = common._request(request, 'username')
        username = re.sub(r'[&=\s]', "", username)
        nickname = common._request(request, 'nickname')
        nickname = re.sub(r'[&=\s]', "", nickname)
        password = common._request(request, 'password')
        role = common._request(request, 'role')
        email = common._request(request, 'email')
        user = models.user.objects.filter(username=username)
        if user:
            result = {'status': 0, 'msg': 'user existed'}
        else:
            models.user(username=username, password=password, nickname=nickname,
                        role=role, email=email).save()
            result = {'status': 1, 'msg': 'create user success'}
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def editUserAPI(cls, request):
        username = common._request(request, 'username')
        username = re.sub(r'[&=\s]', "", username)
        nickname = common._request(request, 'nickname')
        nickname = re.sub(r'[&=\s]', "", nickname)
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
        username = common._request(request, 'username')
        try:
            models.user.objects.filter(username=username).delete()
            result = {'status': 1, 'msg': 'delete user success'}
        except Exception as e:
            result = {'status': 0, 'msg': str(e)}
        return HttpResponse(json.dumps(result), content_type="application/json")


