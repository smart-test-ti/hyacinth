import platform
import os
import re
import sys
import socket
import subprocess
import json
from logzero import logger


def listeningPort(port):
    """
    Detect whether the port is occupied and clean up
    :param port: System port
    :return: None
    """
    if platform.system().lower() != 'windows':
        os.system("lsof -i:%s| grep LISTEN| awk '{print $2}'|xargs kill -9" % port)
    else:
        port_cmd = 'netstat -ano | findstr {}'.format(port)
        r = os.popen(port_cmd)
        r_data_list = r.readlines()
        if len(r_data_list) == 0:
            return
        else:
            pid_list = []
            for line in r_data_list:
                line = line.strip()
                pid = re.findall(r'[1-9]\d*', line)
                pid_list.append(pid[-1])
            pid_set = list(set(pid_list))[0]
            pid_cmd = 'taskkill -PID {} -F'.format(pid_set)
            os.system(pid_cmd)

def getIP():
    """get local ip"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception as e:
        raise e
    finally:
        s.close()
    return ip

def checkPyVer():
    """check python version"""
    if int(platform.python_version().split('.')[0]) < 3:
        logger.error('python version must be >2,your python version is {}'.format(platform.python_version()))
        sys.exit()    

def main(port):
    """main start"""
    try:
        checkPyVer()
        listeningPort(port)
        os.system('python manage.py runserver {ip}:{port}'.format(ip=getIP(), port=port))
    except Exception as e:
        logger.error(e)
    except KeyboardInterrupt:
        logger.info('stop hyacinth success')

if __name__ == '__main__':
    main(60006)