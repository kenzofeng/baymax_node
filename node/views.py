# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import FileResponse, HttpResponse, JsonResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from robot_engine import execute
import os
import env
from robot_engine import utility


@csrf_exempt
def job_start(request, project, test_id):
    report_zip = execute.run_script(request, project, test_id)
    reponse = FileResponse(open(report_zip, 'rb'))
    reponse["filename"] = "%s_%s" % (project, test_id)
    return reponse


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
