from logzero import logger
from django.shortcuts import render,redirect
from functools import wraps
import traceback

class Decorators(object):

    @classmethod
    def check_login(cls,function):
        """login check decorator"""
        @wraps(function)
        def wrap(request, *arg, **kwargs):
            if request.session.get('is_login') == '1' or request.user.username:
                return function(request, *arg, **kwargs)
            else:
                return redirect('/login/signin')
        return wrap

    @classmethod
    def fun_log(cls,function):
        """logging decorator"""
        @wraps(function)
        def wrap(request,*arg, **kwargs):
            func = function(request, *arg, **kwargs)
            logger.info(f'call fun {function.__name__}')
            return  func
        return wrap

    @classmethod
    def catch_except(cls,function):
        """exception jump decorator"""
        @wraps(function)
        def wrap(request,*arg, **kwargs):
            try:
                func = function(request, *arg, **kwargs)
            except:
                traceback.print_exc()
            else:
                return func
        return wrap


