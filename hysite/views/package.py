# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.http import HttpResponse
import json
import re
import random
import string
import sys
import os
import time
from hysite import models
from hysite.public.common import Method
from hysite.public.decorators import Decorators
sys.getdefaultencoding()

common = Method()

class Home:

    currentPath = os.path.dirname(os.path.realpath(__file__))

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def packageInfoPage(cls, request, *arg, **kwargs):
        app = kwargs['app']
        nickname = request.session['nickname']
        username = request.session['username']
        if app in ['all', '']:
            packages = models.package_info.objects.all().order_by('-id')
        else:
            packages = models.package_info.objects.filter(pkgname=app).order_by('-id')
        role = models.user.objects.filter(username=username).values("role").first()['role']
        logo_path = os.path.join(cls.currentPath, "..", "static", "logo")
        android_path = os.path.join(cls.currentPath, "..", "static", "apk")
        ios_path = os.path.join(cls.currentPath, "..", "static", "ipa")
        for path in [android_path,ios_path]:
            if not os.path.exists(path):
                os.mkdir(path)
        return render(request, 'package.html', locals())

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def getPackageAPI(cls, request):
        pkgname = common._request(request, 'pkgname')
        try:
            if pkgname in ['', ' ', None]:
                packages = models.package_info.objects.all().order_by('-id')
            else:
                packages = models.package_info.objects.filter(pkgname=pkgname).order_by('-id')

            packages_list = [{
                'pkgname': package.pkgname,
                'platform': package.platform,
                'key': package.key,
                'icon': package.icon,
                'icon_path': package.icon_path,
                'newest_version': package.newest_version
            } for package in packages]

            result = {'status': 1, 'packages_list': packages_list}
        except Exception as e:
            result = {'status': 0, 'msg': str(e)}
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def createPackageAPI(cls, request):
        username = request.session['username']
        pkgname = common._request(request, 'pkgname')
        pkgname = re.sub(r'[&=\s]', "_", pkgname)
        key = common._request(request, 'key')
        key = re.sub(r'[\u4e00 -\u9fff]', "_", key)
        platform = common._request(request, 'platform')
        icon = common._request(request, 'icon')
        package = models.package_info.objects.filter(pkgname=pkgname)
        try:
            if not package:
                if not key:
                    key = "".join(random.sample(string.ascii_letters+string.digits, 10))
                file_path_dict = {
                    "Android": os.path.join(cls.currentPath, "..", "static", "apk", pkgname),
                    "iOS": os.path.join(cls.currentPath, "..", "static", "ipa", pkgname)
                }
                if not os.path.exists(file_path_dict[platform]):
                    os.mkdir(file_path_dict[platform])
                models.package_info(pkgname=pkgname,
                                    key=key,
                                    creater=username,
                                    platform=platform,
                                    icon=icon).save()
                result = {'status': 1, 'msg': 'create package success'}
            else:
                result = {'status': 0, 'msg': 'package existed'}
        except Exception as e:
            result = {'status': 0, 'msg': str(e)}
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def deletePackageAPI(cls, request):
        pkgname = common._request(request, 'pkgname')
        try:
            icon = models.package_info.objects.filter(pkgname=pkgname).values("icon").first()['icon']
            models.package_info.objects.filter(pkgname=pkgname).delete()
            if icon:
                icon_path = os.path.join(cls.currentPath, "..", "static", "logo", icon)
                if os.path.exists(icon_path):
                    os.remove(icon_path)
            result = {'status': 1, 'msg': 'delete package success'}
        except Exception as e:
            result = {'status': 0, 'msg': str(e)}
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def uploadLogoAPI(cls, request):
        file = request.FILES.get('file')
        filename = common._request(request, 'filename')
        splitext = os.path.splitext(filename)[-1][1:]
        current = time.strftime("%Y%m%d%H%M%S", time.localtime())
        new_file_name = current + '.' + splitext
        logo_path = os.path.join(cls.currentPath, "..", "static", "logo", new_file_name)
        try:
            if not os.path.exists(logo_path):
                common.uploadFile(file_obj=file, file_path=logo_path)
                result = {'status': 1, 'msg': 'success', 'icon': new_file_name}
            else:
                result = {'status': 0, 'msg': 'logo file existed'}
        except Exception as e:
            print(e)
            result = {'status': 0, 'msg': str(e)}
        return HttpResponse(json.dumps(result), content_type="application/json")


class List:

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def packageListPage(cls, request, *arg, **kwargs):
        package = kwargs['package']
        version = kwargs['version']
        nickname = request.session['nickname']
        username = request.session['username']
        role = models.user.objects.filter(username=username).values("role").first()['role']
        return render(request, 'package-list.html', locals())

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def uploadPackageAPI(cls, request):
        file = request.FILES.get('file')
        pkgname = common._request(request, 'pkgname')
        filename = common._request(request, 'filename')
        platform = common._request(request, 'platform')
        path = os.path.dirname(os.path.realpath(__file__))
        file_path_dict = {
            "Android": os.path.join(path, "..", "static", "apk", pkgname, filename),
            "iOS": os.path.join(path, "..", "static", "ipa", pkgname, filename)
        }
        try:
            common.uploadFile(file_obj=file, file_path=file_path_dict[platform])
            result = {'status': 1, 'msg': 'success'}
        except Exception as e:
            result = {'status': 0, 'msg': str(e)}
        return HttpResponse(json.dumps(result), content_type="application/json")

class Manage:

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def packageManagePage(cls, request, *arg, **kwargs):
        nickname = request.session['nickname']
        username = request.session['username']
        role = models.user.objects.filter(username=username).values("role").first()['role']
        packages = models.package_info.objects.all().order_by('-id')
        packages_nums = models.package_info.objects.all().count()
        return render(request, 'package-manage.html', locals())

