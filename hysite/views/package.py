# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.http import HttpResponse
import json
import re
import random
import sys
import os
from hysite import models
from hysite.public.common import Method
from hysite.public.decorators import Decorators
sys.getdefaultencoding()

common = Method()

class Home:

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def packageInfoPage(cls, request):
        nickname = request.session['nickname']
        username = request.session['username']
        role = models.user.objects.filter(username=username).values("role").first()['role']
        packages = models.package_info.objects.all().order_by('-id')
        return render(request, 'package.html', locals())

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def createPackageAPI(cls, request):
        pkgname = common._request(request, 'pkgname')
        pkgname = re.sub(r'[&=\s]', "_", pkgname)
        key = common._request(request, 'key')
        key = re.sub(r'[\u4e00 -\u9fff]', "_", key)
        platform = common._request(request, 'platform')
        icon = common._request(request, 'icon')
        package = models.package_info.objects.filter(pkgname=pkgname)
        if not package:
            if not key:
                key = random.sample('zyxwvutsrqponmlkjihgfedcba', 7)
            path = os.path.dirname(os.path.realpath(__file__))
            file_path_dict = {
                "Android": os.path.join(path, "..", "static", "apk", pkgname),
                "iOS": os.path.join(path, "..", "static", "ipa", pkgname)
            }
            if not os.path.exists(file_path_dict[platform]):
                os.mkdir(file_path_dict[platform])
            models.package_info(pkgname=pkgname, key=key, platform=platform, icon=icon).save()
            result = {'status': 1, 'msg': 'create package success'}
        else:
            result = {'status': 0, 'msg': 'package existed'}
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def uploadLogoAPI(cls, request):
        file = request.FILES.get('file')
        filename = common._request(request, 'filename')
        path = os.path.dirname(os.path.realpath(__file__))
        logo_path = os.path.join(path, "..", "static", "logo", filename)
        try:
            if not os.path.exists(logo_path):
                common.uploadFile(file_obj=file, file_path=logo_path)
                result = {'status': 1, 'msg': 'success', 'icon': filename}
            else:
                result = {'status': 0, 'msg': 'logo file existed'}
        except Exception as e:
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
        # apks = models.package.objects.all().order_by('-id')
        # apk_num = models.package.objects.all().count()
        # paginator = Paginator(apks, 2)
        # page_obj = paginator.get_page(page)
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

