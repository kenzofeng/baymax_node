import os
import sys

import utility
from node import env
import subprocess

mswindows = (sys.platform == "win32")


def run_script(request, project, test_id):
    opath = os.getcwd()
    robot = None
    pid = 0
    try:
        script = request.FILES['script']
        script_path_zip = os.path.join(env.test, request.POST['filename'])
        script_path = os.path.join(env.test, project)
        with open(script_path_zip, 'wb') as sc:
            for chunk in script.chunks():
                sc.write(chunk)
        utility.extract_zip(script_path_zip, script_path)
        reportpath = os.path.join(env.report, "%s_%s" % (project, test_id))
        reportpath_zip = os.path.join(env.report, "%s_%s.zip" % (project, test_id))
        argfile = os.path.join(script_path, 'argfile.txt')
        os.chdir(script_path)
        if mswindows:
            command = "pybot.bat --argumentfile  %s --outputdir %s  %s" % (argfile, reportpath, script_path)
            print command
            robot = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        else:
            command = "pybot --argumentfile %s --outputdir %s  %s" % (argfile, reportpath, script_path)
            robot = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        pid = robot.pid
        while True:
            log = robot.stdout.readline()
            print log
            if robot.poll() is not None:
                break
        utility.zip_file(reportpath,reportpath_zip)
        return reportpath_zip
    except Exception, e:
        print e
    finally:
        os.chdir(opath)
        if robot is not None:
            robot.terminate()
            robot.kill()
        utility.kill(pid)
        utility.remove_file(reportpath)
        utility.remove_file(script_path_zip)
        utility.remove_file(script_path)


