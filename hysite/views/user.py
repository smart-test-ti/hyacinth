# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.http import HttpResponse
from pathlib import Path
import time
import json
import sys
import re
import traceback
import os
import shutil
from hysite import models
from hysite.public.common import Method
from hysite.public.decorators import Decorators
sys.getdefaultencoding()

common = Method()
BASE_DIR = Path(__file__).resolve().parent.parent.parent

class User:

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def userPage(cls, request, *arg, **kwargs):
        nickname = request.session['nickname']
        username = request.session['username']
        role = models.user.objects.filter(username=username).values("role").first()['role']
        avatar = models.user.objects.filter(username=username).values("avatar").first()['avatar']
        users = models.user.objects.filter(~Q(role='超级管理员')).order_by('-id')
        user_nums = models.user.objects.filter(~Q(role='超级管理员')).count()
        return render(request, 'user.html', locals())

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def getUserAPI(cls, request):
        username = common.requestMthod(request, 'username')
        try:
            users = models.user.objects.filter(username=username)
            data = [{'nickname': user.nickname, 'password': user.password,
                     'role': user.role, 'email': user.email, 'ctime': str(user.ctime)} for user in users]
            result = {'status': 1, 'data': data}
        except Exception as e:
            result = {'status': 0, 'msg': str(e)}
            traceback.print_exc()
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def createUserAPI(cls, request):
        username = common.requestMthod(request, 'username')
        username = re.sub(r'[\u4e00 - \u9fff&=\s]', "_", username)
        nickname = common.requestMthod(request, 'nickname')
        nickname = re.sub(r'[&=\s]', "_", nickname)
        password = common.requestMthod(request, 'password')
        role = common.requestMthod(request, 'role')
        email = common.requestMthod(request, 'email')
        user = models.user.objects.filter(username=username)
        if not user:
            models.user(username=username,
                        password=password,
                        nickname=nickname,
                        role=role,
                        email=email).save()
            result = {'status': 1, 'msg': 'create user success'}
        else:
            result = {'status': 0, 'msg': 'user existed'}
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def editUserAPI(cls, request):
        username = common.requestMthod(request, 'username')
        nickname = common.requestMthod(request, 'nickname')
        nickname = re.sub(r'[&=\s]', "_", nickname)
        password = common.requestMthod(request, 'password')
        role = common.requestMthod(request, 'role')
        try:
            models.user.objects.filter(username=username).update(nickname=nickname, password=password, role=role)
            result = {'status': 1, 'msg': 'edit user success'}
        except Exception as e:
            result = {'status': 0, 'msg': str(e)}
            traceback.print_exc()

        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def deleteUserAPI(cls, request):
        username = common.requestMthod(request, 'username')
        try:
            models.user.objects.filter(username=username).delete()
            avatar_user_dir = os.path.join(BASE_DIR, "static", "avatar", username)
            if os.path.exists(avatar_user_dir):
                shutil.rmtree(avatar_user_dir, True)
            result = {'status': 1, 'msg': 'delete user success'}
        except Exception as e:
            result = {'status': 0, 'msg': str(e)}
        return HttpResponse(json.dumps(result), content_type="application/json")

class Setting:

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def settingPage(cls, request, *arg, **kwargs):
        username = request.session['username']
        nickname = models.user.objects.filter(username=username).values("nickname").first()['nickname']
        role = models.user.objects.filter(username=username).values("role").first()['role']
        password = models.user.objects.filter(username=username).values("password").first()['password']
        avatar = models.user.objects.filter(username=username).values("avatar").first()['avatar']
        return render(request, 'setting.html', locals())

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def uploadAvatarAPI(cls, request):
        username = request.session['username']
        file = request.FILES.get('file')
        filename = common.requestMthod(request, 'filename')
        splitext = os.path.splitext(filename)[-1][1:]
        current = time.strftime("%Y%m%d%H%M%S", time.localtime())
        new_file_name = current + '.' + splitext
        avatar_dir = os.path.join(BASE_DIR, "static", "avatar")
        if not os.path.exists(avatar_dir):
            os.mkdir(avatar_dir)
        avatar_user_dir = os.path.join(BASE_DIR, "static", "avatar", username)
        if not os.path.exists(avatar_user_dir):
            os.mkdir(avatar_user_dir)
        avatar_path = os.path.join(BASE_DIR, "static", "avatar", username, new_file_name)
        try:
            if not os.path.exists(avatar_path):
                common.uploadFile(file_obj=file, file_path=avatar_path)
                models.user.objects.filter(username=username).update(avatar=new_file_name)
                result = {'status': 1, 'msg': 'success', 'icon': new_file_name}
            else:
                result = {'status': 0, 'msg': 'avatar file existed'}
        except Exception as e:
            result = {'status': 0, 'msg': str(e)}
            traceback.print_exc()
        return HttpResponse(json.dumps(result), content_type="application/json")


