# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from pathlib import Path
import shutil
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
import traceback

common = Method()
# currentPath = os.path.dirname(os.path.realpath(__file__))
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Home:



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
            logs = models.package_log.objects.all().order_by('-id')[:5]
        role = models.user.objects.filter(username=username).values("role").first()['role']
        avatar = models.user.objects.filter(username=username).values("avatar").first()['avatar']
        logo_path = os.path.join(BASE_DIR, "static", "logo")
        android_path = os.path.join(BASE_DIR, "static", "apk")
        ios_path = os.path.join(BASE_DIR, "static", "ipa")
        for path in [android_path, ios_path]:
            if not os.path.exists(path):
                os.mkdir(path)
        return render(request, 'package.html', locals())

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def getPackageAPI(cls, request):
        pkgname = common.requestMthod(request, 'pkgname')
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
            traceback.print_exc()
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def createPackageAPI(cls, request):
        username = request.session['username']
        pkgname = common.requestMthod(request, 'pkgname')
        pkgname = re.sub(r'[&=\s]', "_", pkgname)
        key = common.requestMthod(request, 'key')
        key = re.sub(r'[\u4e00 -\u9fff]', "_", key)
        platform = common.requestMthod(request, 'platform')
        icon = common.requestMthod(request, 'icon')
        try:
            package = models.package_info.objects.filter(pkgname=pkgname)
            if not package:
                if not key:
                    key = "".join(random.sample(string.ascii_letters+string.digits, 10))
                file_path_dict = {
                    "Android": os.path.join(BASE_DIR, "static", "apk", pkgname),
                    "iOS": os.path.join(BASE_DIR, "static", "ipa", pkgname)
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
            traceback.print_exc()
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def deletePackageAPI(cls, request):
        pkgname = common.requestMthod(request, 'pkgname')
        try:
            file_nums = models.package_list.objects.filter(pkgname=pkgname).count()
            if file_nums == 0:
                platform = models.package_info.objects.filter(pkgname=pkgname).values("platform").first()['platform']
                icon = models.package_info.objects.filter(pkgname=pkgname).values("icon").first()['icon']
                models.package_info.objects.filter(pkgname=pkgname).delete()
                models.package_version_list.objects.filter(pkgname=pkgname).delete()
                if icon:
                    icon_path = os.path.join(BASE_DIR, "static", "logo", icon)
                    if os.path.exists(icon_path):
                        os.remove(icon_path)
                platform_file_dict = {"Android": "apk", "iOS": "ipa"}
                file_path = os.path.join(BASE_DIR, "static", platform_file_dict[platform], pkgname)
                if os.path.exists(file_path):
                    shutil.rmtree(file_path, True)
                result = {'status': 1, 'msg': 'delete package success'}
            else:
                result = {'status': 0, 'msg': 'package files must be 0'}
        except Exception as e:
            result = {'status': 0, 'msg': str(e)}
            traceback.print_exc()
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def uploadLogoAPI(cls, request):
        file = request.FILES.get('file')
        filename = common.requestMthod(request, 'filename')
        splitext = os.path.splitext(filename)[-1][1:]
        current = time.strftime("%Y%m%d%H%M%S", time.localtime())
        new_file_name = current + '.' + splitext
        logo_path = os.path.join(BASE_DIR, "static", "logo", new_file_name)
        try:
            if not os.path.exists(logo_path):
                common.uploadFile(file_obj=file, file_path=logo_path)
                result = {'status': 1, 'msg': 'success', 'icon': new_file_name}
            else:
                result = {'status': 0, 'msg': 'logo file existed'}
        except Exception as e:
            result = {'status': 0, 'msg': str(e)}
            traceback.print_exc()
        return HttpResponse(json.dumps(result), content_type="application/json")


class List:

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def packageListPage(cls, request, *arg, **kwargs):
        app = kwargs['app']
        version = kwargs['version']
        nickname = request.session['nickname']
        username = request.session['username']
        role = models.user.objects.filter(username=username).values("role").first()['role']
        avatar = models.user.objects.filter(username=username).values("avatar").first()['avatar']
        logs = models.package_log.objects.all().order_by('-id')[:5]
        platform = models.package_info.objects.filter(pkgname=app).values("platform").first()['platform']
        file_path_dict = {
            "Android": os.path.join(BASE_DIR, "static", "apk", app, version),
            "iOS": os.path.join(BASE_DIR, "static", "ipa", app, version)
        }
        if not os.path.exists(file_path_dict[platform]) and version != 'None':
            os.mkdir(file_path_dict[platform])

        package_files = models.package_list.objects.filter(pkgname=app, version=version).order_by('-id')
        packages_file_nums = models.package_list.objects.filter(pkgname=app, version=version).count()
        versions = models.package_version_list.objects.filter(pkgname=app).values('version').order_by('-id')
        version_list = [version for version in versions]
        return render(request, 'package-list.html', locals())

    @classmethod
    def packageSharePage(cls, request, *arg, **kwargs):
        token = kwargs['token']
        share_data = models.package_share_info.objects.filter(token=token)
        download_path = None
        if share_data:
            app = models.package_share_info.objects.filter(token=token).values("pkgname").first()['pkgname']
            icon = models.package_info.objects.filter(pkgname=app).values("icon").first()['icon']
            filename = models.package_share_info.objects.filter(token=token).values("filename").first()['filename']
            download_path = models.package_share_info.objects.filter(token=token).values("filepath").first()['filepath']
        return render(request, 'package-share.html', locals())

    @classmethod
    def createVersionFileAPI(cls, request):
        file = request.FILES.get('file')
        key = common.requestMthod(request, 'key')
        version = common.requestMthod(request, 'version')
        build_num = common.requestMthod(request, 'build_num')
        try:
            app = models.package_info.objects.filter(key=key).values("pkgname").first()['pkgname']
            platform = models.package_info.objects.filter(key=key).values("platform").first()['platform']
            platform_file_dict = {"Android": "apk", "iOS": "ipa"}
            if os.path.splitext(file.name)[-1][1:] == platform_file_dict[platform]:
                version_path_dict = {
                    "Android": os.path.join(BASE_DIR, "static", "apk", app, version),
                    "iOS": os.path.join(BASE_DIR, "static", "ipa", app, version)
                }
                if not os.path.exists(version_path_dict[platform]):
                    os.mkdir(version_path_dict[platform])
                file_path_dict = {
                    "Android": os.path.join(BASE_DIR, "static", "apk", app, version, file.name),
                    "iOS": os.path.join(BASE_DIR, "static", "ipa", app, version, file.name)
                }
                if not os.path.exists(file_path_dict[platform]):
                    download_path = '/'.join(['http:/', request.META['HTTP_HOST'], 'static',
                                            platform_file_dict[platform], app, version, file.name])
                    common.uploadFile(file_obj=file, file_path=file_path_dict[platform])
                    models.package_list(pkgname=app,
                                        version=version,
                                        platform=platform,
                                        build_num=build_num,
                                        filename=file.name,
                                        filepath=download_path).save()
                    versions = models.package_version_list.objects.filter(pkgname=app, version=version)
                    if not versions:
                        models.package_version_list(pkgname=app, version=version).save()
                        models.package_info.objects.filter(pkgname=app).update(newest_version=version)
                    models.package_log(username='api', pkgname=app, version=version, action=f'上传文件{filename}').save()
                    result = {'status': 1, 'msg': 'success', 'download_path': download_path}
                else:
                    result = {'status': 0, 'msg': 'filename existed'}
            else:
                result = {'status': 0, 'msg': 'file type is not {}'.format(platform_file_dict[platform])}
        except Exception as e:
            result = {'status': 0, 'msg': str(e)}
            traceback.print_exc()
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    @method_decorator(Decorators.check_login)
    def deleteVersionFileAPI(cls, request):
        pkgname = common.requestMthod(request, 'pkgname')
        version = common.requestMthod(request, 'version')
        filename = common.requestMthod(request, 'filename')
        try:
            platform = models.package_info.objects.filter(pkgname=pkgname).values("platform").first()['platform']
            models.package_list.objects.filter(pkgname=pkgname, version=version, filename=filename).delete()
            models.package_share_info.objects.filter(pkgname=pkgname, version=version).delete()
            platform_file_dict = {"Android": "apk", "iOS": "ipa"}
            file_path = os.path.join(BASE_DIR, "static", platform_file_dict[platform], pkgname, version, filename)
            if os.path.exists(file_path):
                os.remove(file_path)
            result = {'status': 1, 'msg': 'delete package file and share data success'}
        except Exception as e:
            result = {'status': 0, 'msg': str(e)}
            traceback.print_exc()
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    @method_decorator(Decorators.check_login)
    def getPackageVersionAPI(cls, request):
        pkgname = common.requestMthod(request, 'pkgname')
        try:
            versions = models.package_list.objects.filter(pkgname=pkgname).values('version').distinct().order_by('-id')
            version_list = [version for version in versions]
            result = {'status': 1, 'version_list': version_list}
        except Exception as e:
            result = {'status': 0, 'msg': str(e)}
            traceback.print_exc()
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    @method_decorator(Decorators.check_login)
    def createShareLinkAPI(cls, request):
        pkgname = common.requestMthod(request, 'pkgname')
        version = common.requestMthod(request, 'version')
        filename = common.requestMthod(request, 'filename')
        try:
            platform = models.package_info.objects.filter(pkgname=pkgname).values("platform").first()['platform']
            filepath = models.package_list.objects.filter(pkgname=pkgname).values("filepath").first()['filepath']
            token = "".join(random.sample(string.ascii_letters + string.digits, 20))
            models.package_share_info(pkgname=pkgname,
                                      version=version,
                                      platform=platform,
                                      token=token,
                                      filename=filename,
                                      filepath=filepath).save()
            host = request.META['HTTP_HOST']
            share_path = f'http://{host}/package/share/token={token}'
            result = {'status': 1, 'msg': 'success', 'share_path': share_path}
        except Exception as e:
            result = {'status': 0, 'msg': str(e)}
            traceback.print_exc()
        return HttpResponse(json.dumps(result), content_type="application/json")



class Manage:

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def packageManagePage(cls, request, *arg, **kwargs):
        nickname = request.session['nickname']
        username = request.session['username']
        role = models.user.objects.filter(username=username).values("role").first()['role']
        avatar = models.user.objects.filter(username=username).values("avatar").first()['avatar']
        packages = models.package_info.objects.all().order_by('-id')
        packages_nums = models.package_info.objects.all().count()
        logs = models.package_log.objects.all().order_by('-id')[:5]
        return render(request, 'package-manage.html', locals())

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def packageManageVersionPage(cls, request, *arg, **kwargs):
        nickname = request.session['nickname']
        username = request.session['username']
        app = kwargs['app']
        role = models.user.objects.filter(username=username).values("role").first()['role']
        versions = models.package_version_list.objects.filter(pkgname=app).order_by('-id')
        version_nums = models.package_version_list.objects.filter(pkgname=app).count()
        logs = models.package_log.objects.all().order_by('-id')[:5]
        return render(request, 'package-manage-version.html', locals())

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def createVersionAPI(cls, request):
        username = request.session['username']
        pkgname = common.requestMthod(request, 'pkgname')
        version = common.requestMthod(request, 'version')
        try:
            version_nums = models.package_version_list.objects.filter(pkgname=pkgname, version=version).count()
            if version_nums == 0:
                models.package_version_list(pkgname=pkgname, version=version).save()
                models.package_info.objects.filter(pkgname=pkgname).update(newest_version=version)
                models.package_log(username=username, pkgname=pkgname, version=version, action=f'创建新的版本{version}').save()
                result = {'status': 1, 'msg': 'create version success'}
            else:
                result = {'status': 0, 'msg': 'version existed'}
        except Exception as e:
            result = {'status': 0, 'msg': str(e)}
            traceback.print_exc()
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def deleteVersionAPI(cls, request):
        username = request.session['username']
        pkgname = common.requestMthod(request, 'pkgname')
        version = common.requestMthod(request, 'version')
        try:
            file_nums = models.package_list.objects.filter(pkgname=pkgname, version=version).count()
            if file_nums == 0:
                platform = models.package_info.objects.filter(pkgname=pkgname).values("platform").first()['platform']
                models.package_version_list.objects.filter(pkgname=pkgname, version=version).delete()
                platform_file_dict = {"Android": "apk", "iOS": "ipa"}
                file_path = os.path.join(BASE_DIR, "static", platform_file_dict[platform], pkgname, version)
                if os.path.exists(file_path):
                    shutil.rmtree(file_path, True)
                models.package_log(username=username, pkgname=pkgname, version=version, action=f'删除了版本{version}').save()
                result = {'status': 1, 'msg': 'delete version success'}
            else:
                result = {'status': 0, 'msg': 'version files must be 0'}
        except Exception as e:
            result = {'status': 0, 'msg': str(e)}
            traceback.print_exc()
        return HttpResponse(json.dumps(result), content_type="application/json")

    @classmethod
    @method_decorator(Decorators.check_login)
    @method_decorator(Decorators.catch_except)
    def editVersionAPI(cls, request):
        username = request.session['username']
        pkgname = common.requestMthod(request, 'pkgname')
        old_version = common.requestMthod(request, 'old_version')
        new_version = common.requestMthod(request, 'new_version')
        try:
            version_nums = models.package_version_list.objects.filter(pkgname=pkgname, version=new_version).count()
            if version_nums == 0:
                models.package_version_list.objects.filter(pkgname=pkgname, version=old_version).update(version=new_version)
                models.package_list.objects.filter(pkgname=pkgname, version=old_version).update(version=new_version)
                models.package_log(username=username, pkgname=pkgname, version=old_version, action=f'{old_version}修改为{new_version}').save()
                result = {'status': 1, 'msg': 'edit version success'}
            else:
                result = {'status': 0, 'msg': 'version existed'}
        except Exception as e:
            result = {'status': 0, 'msg': str(e)}
            traceback.print_exc()

        return HttpResponse(json.dumps(result), content_type="application/json")

