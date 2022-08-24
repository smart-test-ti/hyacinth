# -*- coding:utf-8 -*-
from . import *


class INFO(View):

    apk_file_path = '/home1/www/tomcat/apache-tomcat-9.0.27/webapps/examples/stest/apk/'

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def apk_info_page(cls,request,*arg,**kwargs):
        page = int(kwargs['page'])
        if request.user.username:
            user_type = 'github'
            username = request.user.username
        else:
            user_type = 'elver'
            username = request.session['username']
            avatar = models.User.objects.filter(username=username).values("avatar").last()['avatar']
        apks = models.APK.objects.all().order_by('-id')
        apk_num = models.APK.objects.all().count()
        paginator = Paginator(apks, 2)
        page_obj = paginator.get_page(page)
        return render(request, 'elver/apk/apk_info.html',locals())

    @classmethod
    @method_decorator(Decorators.catch_except)
    def create_apk_info_api(cls, request):
        """创建apk信息接口"""
        project = common.request_method(request, "project")
        apkname = common.request_method(request, "apkname")
        env = common.request_method(request, "env")
        platform = common.request_method(request, "platform")
        version = common.request_method(request, "version")
        size = common.request_method(request, "size")
        apklink = common.request_method(request, "apklink")
        try:
            models.APK(apkname=apkname,project=project,env=env,platform=platform,version=version,size=size,apklink=apklink).save()
        except Exception as e:
            result = {'status': 0, 'msg':f'上传apk失败:{str(e)}'}
            return HttpResponse(json.dumps(result), content_type="application/json")
        else:
            result = {'status': 1, 'msg': '创建APK成功'}    
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    @method_decorator(Decorators.catch_except)
    def upload_apk_api(cls, request):
        """上传apk文件接口"""
        file_obj = request.FILES.get('file')
        apkname = common.request_method(request, "apkname")
        apk_num = models.APK.objects.filter(apkname=apkname).count()
        if apk_num == 0:
            apkname = common.replace_name(apkname)
            try:
                common.save_upload_file(cls.apk_file_path+apkname,file_obj)
            except Exception as e:
                result = {'status': 0, 'msg':f'上传apk失败:{str(e)}'}
                return HttpResponse(json.dumps(result), content_type="application/json")
            else:
                apklink = f'http://47.106.194.167:8181/stest/apk/{apkname}'
                result = {'status': 1, 'msg': '创建APK成功','apklink':apklink,'apkname':apkname}
        else:
            result = {'status': 0, 'msg': '该APK名称已存在'}
        return HttpResponse(json.dumps(result), content_type="application/json")    

    @classmethod
    @method_decorator(Decorators.catch_except)
    def edit_apk_info_api(cls, request):
        """编辑apk信息接口"""
        apkname = common.request_method(request, "apkname")
        project = common.request_method(request, "project")
        env = common.request_method(request, "env")
        platform = common.request_method(request, "platform")
        version = common.request_method(request, "version")
        size = common.request_method(request, "size")
        ctime = time.strftime("%Y-%m-%d %H:%M", time.localtime())
        try:
            models.APK.objects.filter(apkname=apkname).update(project=project,env=env,platform=platform,
                                                              version=version,size=size, ctime=ctime)
            result = {'status': 1, 'msg': '更新成功！'}
        except Exception as e:
            result = {'status': 0, 'msg': str(e)}
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    @method_decorator(Decorators.catch_except)
    def delete_apk_info_api(cls, request):
        """删除apk信息接口"""
        apkname = common.request_method(request, "apkname")
        try:
            models.APK.objects.filter(apkname=apkname).delete()
            os.remove(cls.apk_file_path+apkname)
            result = {'status': 1, 'msg': '删除成功！'}
        except Exception as e:
            result = {'status': 0, 'msg': str(e)}
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    @method_decorator(Decorators.catch_except)
    def get_apk_info_api(cls,request):
        """获取apk信息api"""
        apkname = common.request_method(request, "apkname")
        try:
            apk_info = common.get_apk_info(cls.apk_file_path+apkname)
            result = {'status': 1, 'apk_info': apk_info}
        except Exception as e:
            result = {'status': 0, 'msg': str(e)}
        return HttpResponse(json.dumps(result), content_type="application/json")


class VIRUS_SCAN(View):

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def virus_scan_page(cls,request):
        if request.user.username:
            user_type = 'github'
            username = request.user.username
        else:
            user_type = 'elver'
            username = request.session['username']
            avatar = models.User.objects.filter(username=username).values("avatar").last()['avatar']
        return render(request, 'elver/apk/virus_scan.html',locals())

class REINFORCE(View):

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def reinforce_page(cls,request):
        if request.user.username:
            user_type = 'github'
            username = request.user.username
        else:
            user_type = 'elver'
            username = request.session['username']
            avatar = models.User.objects.filter(username=username).values("avatar").last()['avatar']
        return render(request, 'elver/apk/reinforce.html',locals())
