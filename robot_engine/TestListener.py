from robot.api import logger


class TestListener:
    ROBOT_LISTENER_API_VERSION = 2

    def start_keyword(self, name, attrs):
        logger.console('Start Keyword:{}.{}'.format(name, " ".join(attrs['args'])))

    def start_suite(self, name, attrs):
        logger.console('Start Suite:{}'.format(name))
