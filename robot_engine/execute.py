import logging
import os
import shlex
import subprocess
import threading
import requests

import utility
from mylogger import Mylogger
from node import env

logger = logging.getLogger('django')


def get_robot_log(robot,mylog):
    while True:
        log = robot.stdout.readline()
        mylog.robot_info(log.replace('\r\n', ''))
        if 'Report:' in log and 'report.html' in log:
            break
        if robot.poll() is not None:
            break


def run_script(request, project, test_id):
    opath = os.getcwd()
    pid = 0
    reportpath_zip = ""
    try:
        mylog = Mylogger(os.path.join(env.log, test_id))
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
        robot = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        pid = robot.pid
        r = threading.Thread(target=get_robot_log, args=(robot,mylog))
        r.start()
        r.join()
        try:
            if robot is not None:
                # robot.terminate()
                # robot.kill()
                os.killpg(os.getpgid(robot.pid), 9)
        except Exception:
            pass
        utility.zip_file(reportpath, reportpath_zip)
    except Exception, e:
        logger.error(e)
        mylog.robot_info(e)
    finally:
        os.chdir(opath)
        utility.kill(pid)
        utility.remove_file(reportpath)
        utility.remove_file(script_path_zip)
        # utility.remove_file(script_path)
        return reportpath_zip
