from apscheduler.schedulers.background import BackgroundScheduler
import os
import subprocess
import shlex

scheduler = BackgroundScheduler()
scheduler.start()


def execute_shell():
    print 'execute_shell'
    Base_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    Shell_DIR = os.path.join(Base_DIR, "shell")
    for dirpath, dirnames, filenames in os.walk(Shell_DIR):
        for filename in filenames:
            f = os.path.join(dirpath, filename)
            command = "sh {}".format(f)
            print command
            log = open(os.path.join(Shell_DIR, "{}.log".format(filename)), 'w')
            subprocess.call(shlex.split(command), stdout=log, stderr=subprocess.STDOUT)


scheduler.add_job(execute_shell, 'interval', minutes=5)
print("Scheduler started!")
