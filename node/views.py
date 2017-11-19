# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse
from django.http import StreamingHttpResponse,FileResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
import json
from robot_engine import execute

@csrf_exempt
def job_start(request, project, test_id):
    report_zip = execute.run_script(request,project,test_id)
    reponse = FileResponse(open(report_zip, 'rb'))
    reponse["filename"]="%s_%s"%(project,test_id)
    return reponse
