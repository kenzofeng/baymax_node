import os

import utility
from node import env
import subprocess


def run_script(request, project, test_id):
    opath = os.getcwd()
    pid = 0
    reportpath_zip = ""
    try:
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
        command = "python -m robot.run --argumentfile %s --outputdir %s  %s" % (argfile, reportpath, script_path)
        utility.logmsgs(os.path.join(env.log, test_id), command)
        robot = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        pid = robot.pid
        while True:
            log = robot.stdout.readline()
            utility.logmsgs(os.path.join(env.log, test_id), log.replace('\r\n', ''))
            if robot.poll() is not None:
                break
        utility.zip_file(reportpath, reportpath_zip)
    except Exception, e:
        utility.logmsgs(os.path.join(env.log, test_id), e)
    finally:
        os.chdir(opath)
        utility.kill(pid)
        utility.remove_file(reportpath)
        utility.remove_file(script_path_zip)
        # utility.remove_file(script_path)
        return reportpath_zip
