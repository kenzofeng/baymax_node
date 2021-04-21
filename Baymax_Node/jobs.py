import logging
import os
import shlex
import subprocess

import requests
from apscheduler.schedulers.background import BackgroundScheduler

logger = logging.getLogger('django')
scheduler = BackgroundScheduler()
scheduler.start()
logpath = '/usr/local/logs'
Base_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def execute_shell():
    Shell_DIR = os.path.join(Base_DIR, "shell")
    for dirpath, dirnames, filenames in os.walk(Shell_DIR):
        for filename in filenames:
            f = os.path.join(dirpath, filename)
            command = "sh {}".format(f)
            subprocess.call(shlex.split(command))
            logger.info("execute_shell fiel:{}".format(f))


def register_server():
    try:
        instance_id = os.environ["POD_NAME"]
        public_ip = ""
        private_ip = os.environ["POD_IP"]
        server_url = os.environ["BAYMAX_SERVER"]
        res = requests.post('{}/api/register/'.format(server_url),
                            json={"instance_id": instance_id, "private_ip": private_ip, "public_ip": public_ip,
                                  "name": instance_id}, timeout=5)
        logger.info("Register Server Info:{}".format(res.json()))
    except Exception as e:
        logger.error("Register Server Error:{}".format(e))


scheduler.add_job(execute_shell)
scheduler.add_job(register_server)
