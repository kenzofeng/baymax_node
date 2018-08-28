import logging


class Mylogger():
    def __init__(self, path):
        self.path = path
        self.logger_robot = logging.getLogger('robot')
        self.logger_app = logging.getLogger('app')

    def init_logger(self):
        rf = logging.FileHandler(self.path)
        af = logging.FileHandler(self.path)
        fmt = "%(name)s : %(message)s"
        formatter = logging.Formatter(fmt)
        rf.setFormatter(formatter)
        af.setFormatter(formatter)
        self.logger_robot.addFilter(rf)
        self.logger_app.addFilter(af)

    def robot_info(self, msg):
        self.logger_robot.info(msg)

    def robot_error(self, msg):
        self.logger_robot.error(msg)

    def app_info(self, msg):
        self.logger_app.info(msg)

    def app_error(self, msg):
        self.logger_app.error(msg)
