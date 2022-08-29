# -*- coding:utf-8 -*-
from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
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

class Manage:

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def packageInfoPage(cls, request, *arg, **kwargs):
        page = int(kwargs['page'])
        nickname = request.session['nickname']
        # apks = models.package.objects.all().order_by('-id')
        # apk_num = models.package.objects.all().count()
        # paginator = Paginator(apks, 2)
        # page_obj = paginator.get_page(page)
        return render(request, 'package.html', locals())

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def packageListPage(cls, request, *arg, **kwargs):
        page = int(kwargs['page'])
        nickname = request.session['nickname']
        # apks = models.package.objects.all().order_by('-id')
        # apk_num = models.package.objects.all().count()
        # paginator = Paginator(apks, 2)
        # page_obj = paginator.get_page(page)
        return render(request, 'package-list.html', locals())