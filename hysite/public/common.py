import datetime
import requests
import os
from hysite import models
import pymysql
from androguard.core.bytecodes.apk import APK
pymysql.install_as_MySQLdb()

class Method(object):

    @classmethod
    def __init__(cls):
        cls.headers = {
            'User-Agent': 'User-Agent:Mozilla/5.0',
            'Content-Type': "application/x-www-form-urlencoded",
            'Cache-Control': "no-cache"
        }

    @classmethod
    def _request(cls, request, object):
        """请求方法"""
        if request.method == "POST":
            return request.POST.get(object)
        else:
            return request.GET.get(object)

    @classmethod
    def getfileList(cls, file_dir: str):
        """
        :brief:获取文件夹下内，所有文件
        :param file_dir:文件夹目录
        :return: 文件列表
        """
        for root, dirs, files in os.walk(file_dir):
            return files
        else:
            return None

    @classmethod
    def getDatesByTimes(cls, sDateStr: str, eDateStr: str) -> list:
        """获取区间日期"""
        date_list = []
        datestart = datetime.datetime.strptime(sDateStr, '%Y-%m-%d')
        dateend = datetime.datetime.strptime(eDateStr, '%Y-%m-%d')
        date_list.append(datestart.strftime('%Y-%m-%d'))
        while datestart < dateend:
            datestart += datetime.timedelta(days=1)
            date_list.append(datestart.strftime('%Y-%m-%d'))
        return date_list

    @classmethod
    def mysqlConnect(cls, host, port, user, password, db):
        """mysql连接"""
        conn = pymysql.connect(host=host, port=port, user=user, passwd=password, db=db, charset='utf8')
        cursor = conn.cursor()
        return cursor, conn

    @classmethod
    def getApkInfo(cls, apk_path: str) -> dict:
        """获取apk信息"""
        apk_info = {}
        androguard = APK(apk_path)
        if androguard.is_valid_APK():
            apk_info['app'] = androguard.get_app_name()
            apk_info['pkgname'] = androguard.get_package()
            apk_info['version_code'] = androguard.get_androidversion_code()
            apk_info['version_name'] = androguard.get_androidversion_name()
            apk_info['main_activity'] = androguard.get_main_activity()
        return apk_info

    @classmethod
    def addUserLog(cls, username, **kwargs):
        """记录用户操作日志"""
        avatar = kwargs['avatar']
        page = kwargs['page']
        action = kwargs['action']
        content = kwargs['content']
        models.Log.objects.create(username=username, avatar=avatar, page=page, action=action, content=content)

    @classmethod
    def uploadFile(cls, file_path, file_obj):
        """保存上传文件"""
        with open(file_path, 'wb+') as f:
            for chunk in file_obj.chunks():
                f.write(chunk)