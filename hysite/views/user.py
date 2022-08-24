# -*- coding:utf-8 -*-
from . import *


class Setting(View):

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def setting_page(cls,request):
        if request.user.username:
            user_type = 'github'
            username = request.user.username
        else:
            user_type = 'elver'
            username = request.session['username']
            avatar = models.User.objects.filter(username=username).values("avatar").last()['avatar']
        return render(request, 'elver/other/setting.html',locals())

class UserActivity(View):

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def user_activity_page(cls,request):
        if request.user.username:
            user_type = 'github'
            username = request.user.username
        else:
            user_type = 'elver'
            username = request.session['username']
            avatar = models.User.objects.filter(username=username).values("avatar").last()['avatar']
        return render(request, 'elver/other/activity.html',locals())
