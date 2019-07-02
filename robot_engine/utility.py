import logging
import os
import signal
import socket
import sys
import zipfile

import requests
from django.conf import settings

mswindows = (sys.platform == "win32")
logger = logging.getLogger('django')


def get_instance_id():
    try:
        rs = requests.get(settings.EC2_META_DATA_URL, timeout=5)
        return rs.content
    except Exception:
        return None


def get_ip():
    private_ip = socket.gethostbyname(socket.gethostname())
    rs = requests.get("http://httpbin.org/ip")
    public_ip = rs.json()['origin'].split(',')[0]
    return private_ip, public_ip


def remove_file(fpath):
    if os.path.exists(fpath):
        try:
            os.remove(fpath)
        except Exception as e:
            print e
        try:
            if os.path.exists(fpath):
                if mswindows:
                    os.system('rd /S/Q %s' % fpath)
                else:
                    os.system('rm -rf %s' % fpath)
        except Exception as e:
            print e


def zip_file(sourcefile, targetfile):
    filelist = []
    if os.path.isfile(sourcefile):
        filelist.append(sourcefile)
    else:
        for root, dirs, files in os.walk(sourcefile):
            for name in files:
                filelist.append(os.path.join(root, name))
    zf = zipfile.ZipFile(targetfile, "w", zipfile.zlib.DEFLATED, allowZip64=True)
    for tar in filelist:
        arcname = tar[len(sourcefile):]
        zf.write(tar, arcname)
    zf.close()


def kill(p):
    if p is None:
        return
    else:
        logger.info(p.pid)
        try:
            # os.killpg(os.getpgid(pid), 9)
            os.killpg(p.pid, signal.SIGUSR1)
            # os.kill(pid, signal.SIGTERM)
        except Exception as e:
            logger.error(e)


def extract_zip(source, target):
    f = zipfile.ZipFile(source, 'r', allowZip64=True)
    for ff in f.namelist():
        f.extract(ff, target)
