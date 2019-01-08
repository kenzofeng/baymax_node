from robot.api import logger


class TestListener:
    ROBOT_LISTENER_API_VERSION = 2

    def start_keyword(self, name, attrs):
        logger.console('Start Keyword:{}.{}'.format(name, attrs['args'][0]))

    def end_keyword(self, name, attrs):
        logger.console('End Keyword:{}.{}'.format(name, attrs['args'][0]))

    # def start_suite(self, name, attrs):
    #     logger.console('Start Suite:{}'.format(name))
