from logzero import logger
from django.shortcuts import render,redirect
from functools import wraps
import traceback

class Decorators(object):

    @classmethod
    def _check_login(cls,function):
        """登录检查装饰器"""
        @wraps(function)
        def wrap(request, *arg, **kwargs):
            if request.session.get('is_login') == '1' or request.user.username:
                return function(request, *arg, **kwargs)
            else:
                return redirect('/login/signin')
        return wrap

    @classmethod
    def _fun_log(cls,function):
        """记录日志装饰器"""
        @wraps(function)
        def wrap(request,*arg, **kwargs):
            func = function(request, *arg, **kwargs)
            logger.info(f'call fun {function.__name__}')
            return  func
        return wrap

    @classmethod
    def _catch_except(cls,function):
        """异常跳转装饰器"""
        @wraps(function)
        def wrap(request,*arg, **kwargs):
            try:
                func = function(request, *arg, **kwargs)
            except:
                traceback.print_exc()
            else:
                return func
        return wrap


