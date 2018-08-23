# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import shlex

from django.http import FileResponse, HttpResponse, JsonResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from robot_engine import execute
import os
import env
from robot_engine import utility
import subprocess


def status(request):
    return JsonResponse({"status": "200"})


@csrf_exempt
def job_start(request, project, test_id):
    try:
        # report_zip = execute.run_script(request, project, test_id)
        # reponse = FileResponse(open(report_zip, 'rb'))
        # reponse["filename"] = "%s_%s" % (project, test_id)
        # return reponse
        opath = os.getcwd()
        # script = request.FILES['script']
        return HttpResponse(opath, content_type='text/html')
    except Exception as e:
        return HttpResponse(e, content_type='text/html')

def job_stop(request):
    command = "ps -ef|grep 'python -m' |awk '{print $2}'|xargs kill -9"
    stop = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    rs = stop.stdout.read()
    return HttpResponse(rs, content_type='text/html')


def test_run_raw_log(request, logid):
    fst = "no log"
    try:
        logpath = os.path.join(env.log, logid)
        if os.path.exists(logpath):
            f = open(logpath, 'r')
            fst = f.read()
            f.close()
    except Exception, e:
        return HttpResponse(e)
    return HttpResponse(fst, content_type='text/html')


def test_run_log(request, logid):
    joblog = ""
    try:
        logpath = os.path.join(env.log, logid)
        if os.path.exists(logpath):
            f = open(logpath, 'r')
            fst = f.read()
            f.close()
            for l in fst.split('\n'):
                joblog = joblog + "<span>%s</span><br/>" % (l)
    except Exception, e:
        return HttpResponse(e)
    return HttpResponse(joblog, content_type='text/html')


def test_run_log_delete(request, logid):
    logpath = os.path.join(env.log, logid)
    if os.path.exists(logpath):
        utility.remove_file(logpath)
    reportpath_zip = os.path.join(env.report, "%s.zip" % logid)
    if os.path.exists(reportpath_zip):
        utility.remove_file(reportpath_zip)
    return JsonResponse({'status': "success"})
