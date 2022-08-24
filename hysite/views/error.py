# -*- coding:utf-8 -*-
from . import *

class CommonError(View):

    @classmethod
    def error_404_page(cls,request,exception):
        return render(request, 'elver/error/404.html')

    @classmethod
    def error_500_page(cls, request):
        return render(request, 'elver/error/500.html')
