import logging
import os


class Mylogger():
    def __init__(self, path, apps):
        self.path = path
        self.apps = apps
        self.logger_robot = None
        self.init_logger()

    def init_logger(self):
        rf = logging.FileHandler(self.path)
        fmt = "%(name)s : %(message)s"
        formatter = logging.Formatter(fmt)
        rf.setFormatter(formatter)
        self.logger_robot = logging.getLogger('robot')
        self.logger_robot.setLevel(logging.INFO)
        self.logger_robot.addHandler(rf)
        for app in self.apps:
            setattr(self, app, logging.getLogger(app))
            getattr(self, app).setLevel(logging.INFO)
            getattr(self, app).addHandler(rf)

    def robot_info(self, msg):
        self.logger_robot.info(msg)

    def robot_error(self, msg):
        self.logger_robot.error(msg)

    def app_info(self, app, msg):
        getattr(self, app).info(msg.encode("utf-8"))

    def app_error(self, app, msg):
        getattr(self, app).error(msg.encode("utf-8"))
