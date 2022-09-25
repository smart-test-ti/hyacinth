# -*- coding:utf-8 -*-
from django.shortcuts import render
import sys
from hysite.public.common import Method
sys.getdefaultencoding()
sys.getdefaultencoding()

common = Method()

class Error():

    @classmethod
    def error_404_page(cls,request, exception):
        return render(request, '404.html')

    @classmethod
    def error_500_page(cls, request):
        return render(request, '500.html')
