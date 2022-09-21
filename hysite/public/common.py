import datetime
import time
import os
import re
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
    def requestMthod(cls, request, object):
        """request method"""
        if request.method == "POST":
            return request.POST.get(object)
        else:
            return request.GET.get(object)

    def isInvaild(cls, check_str):
        """Determine whether it contains illegal characters"""
        searchObj = re.search(r'[&=\s\u4e00-\u9fff]', check_str, re.M | re.I)
        if searchObj:
            return True
        return False

    @classmethod
    def currentTime(cls):
        """get current time"""
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    @classmethod
    def getfileList(cls, file_dir: str):
        """Get a list of files in a directory"""
        for root, dirs, files in os.walk(file_dir):
            return files
        else:
            return None

    @classmethod
    def getDatesByTimes(cls, sDateStr: str, eDateStr: str) -> list:
        """Get interval date"""
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
        """mysql connect"""
        conn = pymysql.connect(host=host, port=port, user=user, passwd=password, db=db, charset='utf8')
        cursor = conn.cursor()
        return cursor, conn

    @classmethod
    def getApkInfo(cls, apk_path: str) -> dict:
        """get apk info"""
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
        """Record user operation log"""
        avatar = kwargs['avatar']
        page = kwargs['page']
        action = kwargs['action']
        content = kwargs['content']
        models.Log.objects.create(username=username, avatar=avatar, page=page, action=action, content=content)

    @classmethod
    def uploadFile(cls, file_path, file_obj):
        """save upload file"""
        with open(file_path, 'wb+') as f:
            for chunk in file_obj.chunks():
                f.write(chunk)