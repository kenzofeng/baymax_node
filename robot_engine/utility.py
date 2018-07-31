import os
import random
import re
import signal
import sys
import zipfile
import zlib
from datetime import *

import svn.local

from node import env

mswindows = (sys.platform == "win32")


def rendestring(string):
    if string != "":
        _variable_pattern = r'\$\{[^\}]+\}'
        match = re.findall(_variable_pattern, string)
        if match:
            for arg in match:
                string = string.replace(arg, str(get_variable_value(arg)))
        return string


def matchre(path):
    warpath = os.path.split(path)
    filelist = os.listdir(warpath[0])
    for f in filelist:
        if warpath[-1] == f:
            return os.path.join(warpath[0], f)
        pattern = re.compile(warpath[-1].replace('$', '\\'))
        match = pattern.match(f)
        if match:
            return os.path.join(warpath[0], match.group())


def get_variable_value(arg):
    if env.variables.has_key(arg):
        return env.variables[arg]
    else:
        return arg


def gettoday():
    return datetime.now().strftime('%Y%m%d')


def getnow():
    return datetime.now().strftime('%H%M%S')


def gettime(format='%Y-%m-%d %H:%M:%S'):
    return datetime.now().strftime(format)


def mkdir(dirpath):
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)


def logmsgs(logpath, msgs):
    f = open(os.path.join(env.log, logpath), 'a')
    f.writelines(msgs)
    f.write('\n')
    f.close()


def logmsg(logpath, msg):
    f = open(os.path.join(env.log, logpath), 'a')
    f.write(msg)
    f.write('\n')
    f.close()


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


def save_test_log(test):
    log_path = os.path.join(env.log, test.test_log.path)
    f = open(log_path, 'rb')
    fstr = f.read()
    f.close()
    gzipstr = zlib.compress(fstr)
    test.test_log.text = gzipstr.encode("base64")
    test.test_log.save()
    remove_file(log_path)


def save_log(job):
    log_path = os.path.join(env.log, job.log.path)
    f = open(log_path, 'rb')
    fstr = f.read()
    f.close()
    gzipstr = zlib.compress(fstr)
    job.log.text = gzipstr.encode("base64")
    job.log.save()
    remove_file(log_path)


def update_Doraemon():
    D = svn.local.LocalClient(env.Doraemon)
    D.update()


def zip_file(sourcefile, targetfile):
    filelist = []
    if os.path.isfile(sourcefile):
        filelist.append(sourcefile)
    else:
        for root, dirs, files in os.walk(sourcefile):
            for name in files:
                filelist.append(os.path.join(root, name))
    zf = zipfile.ZipFile(targetfile, "w", zipfile.zlib.DEFLATED)
    for tar in filelist:
        arcname = tar[len(sourcefile):]
        zf.write(tar, arcname)
    zf.close()


def kill(pid):
    try:
        os.kill(pid, signal.SIGTERM)
    except Exception:
        pass


def extract_zip(source, target):
    f = zipfile.ZipFile(source, 'r')
    for ff in f.namelist():
        f.extract(ff, target)


def random_str(randomlength=15):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


def conver_To_Boolean(value):
    if value.lower() == "true":
        return True
    else:
        return False
