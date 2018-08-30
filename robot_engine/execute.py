import logging
import os
import shlex
import subprocess
import threading
import requests
import time
import utility
from mylogger import Mylogger
from node import env

logger = logging.getLogger('django')


def tailf(filename):
    f = open(filename, 'r')
    f.seek(0, 2)
    while True:
        line = f.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line


def get_app_log(app, app_log, mylog, stop_event):
    if app_log:
        for i in tailf(app_log):
            mylog.app_info(app, i)
            if stop_event.is_set():
                return


def get_robot_log(robot, mylog):
    while True:
        log = robot.stdout.readline()
        mylog.robot_info(log.replace('\r\n', ''))
        if 'Report:' in log and 'report.html' in log:
            break
        if robot.poll() is not None:
            break


def run_script(request, project, test_id):
    opath = os.getcwd()
    reportpath_zip = ""
    try:
        applogs = request.POST['app'].split(";")
        apps = [os.path.splitext(os.path.basename(applog))[0] for applog in applogs]
        mylog = Mylogger(os.path.join(env.log, test_id), apps)
        mylog.robot_info("ip:%s id:%s" % (requests.get('http://ip.42.pl/raw').text, test_id))
        script = request.FILES['script']
        script_path_zip = os.path.join(env.test, request.POST['filename'])
        script_path = os.path.join(env.test, project)
        utility.remove_file(script_path)
        utility.remove_file(script_path_zip)
        reportpath = os.path.join(env.report, "%s_%s" % (project, test_id))
        reportpath_zip = os.path.join(env.report, "%s.zip" % test_id)
        utility.remove_file(reportpath)
        utility.remove_file(reportpath_zip)
        with open(script_path_zip, 'wb') as sc:
            for chunk in script.chunks():
                sc.write(chunk)
        utility.extract_zip(script_path_zip, script_path)
        argfile = os.path.join(script_path, 'argfile.txt')
        os.chdir(script_path)
        os.system('chmod 777 -R *')
        if os.path.exists(argfile):
            command = "python -m robot.run --argumentfile %s --outputdir %s  %s" % (argfile, reportpath, script_path)
        else:
            command = "python -m robot.run --outputdir %s  %s" % (argfile, reportpath, script_path)
        mylog.robot_info(command)
        robot = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True,
                                 preexec_fn=os.setsid)
        a_stop = threading.Event()
        for app, applog in zip(apps, applogs):
            mylog.robot_info("app:{} log:{}".format(app,applog))
            a = threading.Thread(target=get_app_log, args=(app, applog, mylog, a_stop))
            a.start()
        r = threading.Thread(target=get_robot_log, args=(robot, mylog))
        r.start()
        r.join()
        a_stop.set()
        utility.zip_file(reportpath, reportpath_zip)
        utility.kill(robot)
    except Exception, e:
        logger.error(e)
        mylog.robot_info(e)
    finally:
        os.chdir(opath)
        utility.remove_file(reportpath)
        utility.remove_file(script_path_zip)
        # utility.remove_file(script_path)
        return reportpath_zip
