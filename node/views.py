# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import os
import shlex
from subprocess import Popen, PIPE, STDOUT

from django.http import FileResponse, HttpResponse, JsonResponse
from Baymax_Node.jobs import *
from django.views.decorators.csrf import csrf_exempt

from django.views.decorators.gzip import gzip_page
import env
from robot_engine import execute
from robot_engine import utility
import json

logger = logging.getLogger('django')


def status(request):
    return JsonResponse({"status": "200"})


@csrf_exempt
def version(request):
    result_str = ""
    data = json.loads(request.body)
    path = data['path']
    if path:
        paths = path.split(";")
        for path in paths:
            result_str += (path + '\n')
            p = Popen(shlex.split("grep -E 'git.branch|git.commit.id=' {}".format(path)), stdout=PIPE, stderr=STDOUT)
            output = p.stdout.read()
            result_str += output.decode('utf-8')
    return HttpResponse(result_str, content_type='text/html')


@csrf_exempt
def job_start(request, project, test_id):
    try:
        report_zip = execute.run_script(request, project, test_id)
        response = FileResponse(open(report_zip, 'rb'))
        response["filename"] = "%s_%s" % (project, test_id)
        return response
    except Exception as e:
        return HttpResponse(e, content_type='text/html')


def job_stop(request):
    command = "ps -ef|grep 'python -m' |awk '{print $2}'|xargs kill -9"
    stop = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    rs = stop.stdout.read()
    return HttpResponse(rs, content_type='text/html')


@gzip_page
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
    return HttpResponse(fst)


@gzip_page
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
    return HttpResponse(joblog)


def test_run_log_delete(request, logid):
    logpath = os.path.join(env.log, logid)
    if os.path.exists(logpath):
        utility.remove_file(logpath)
    reportpath_zip = os.path.join(env.report, "%s.zip" % logid)
    if os.path.exists(reportpath_zip):
        utility.remove_file(reportpath_zip)
    return JsonResponse({'status': "success"})
