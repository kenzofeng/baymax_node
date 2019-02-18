import logging
import os
import shlex
import subprocess
import ConfigParser
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
import socket
import uuid

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
            log = open(os.path.join(logpath, "{}.log".format(filename)), 'w')
            subprocess.call(shlex.split(command), stdout=log, stderr=subprocess.STDOUT)


def get_instance_id():
    try:
        rs = requests.get(settings.EC2_META_DATA_URL, timeout=5)
        return rs.content
    except Exception:
        return None


def get_ip():
    private_ip = socket.gethostbyname(socket.gethostname())
    rs = requests.get("http://httpbin.org/ip")
    public_ip = rs.json()['origin'].split(',')[0]
    return private_ip, public_ip


def register_server():
    server_ini = os.path.join(Base_DIR, "server.ini")
    if os.path.exists(server_ini):
        config = ConfigParser.ConfigParser()
        config.read(server_ini)

        try:
            instance_id = config.get('Server', 'instance_id', None)
        except Exception:
            instance_id = get_instance_id() or str(uuid.uuid1())
            config.set('Server', 'instance_id', instance_id)
            config.write(open(server_ini, 'wb'))
        node_name = "{}_{}".format(config.get('Server', 'name'), instance_id)
        private_ip, public_ip = get_ip()
        server_url = settings.SERVER_URL
        try:
            requests.post('{}/api/register/'.format(server_url),
                          json={"instance_id": instance_id, "private_ip": private_ip, "public_ip": public_ip,
                                "name": node_name}, timeout=5)
        except Exception as e:
            logger.error("Register Server Error:{}".format(e))
    else:
        logger.error("Register Server ini is not found")


scheduler.add_job(execute_shell)
scheduler.add_job(register_server)
