from robot.api import logger


class TestListener:
    ROBOT_LISTENER_API_VERSION = 2

    def start_keyword(self, name, attrs):
        logger.console('Start Keyword:{}'.format(name))

    # def end_keyword(self, name, attrs):
    #     logger.console('End Keyword:{}'.format(name))

    def start_test(self, name, attrs):
        logger.console('Start Test:{} Starttime:{}'.format(name, attrs['starttime']))

    def end_test(self, name, attrs):
        logger.console(
            'End Test:{} Status:{}'.format(name, attrs['status']))

    # def start_suite(self, name, attrs):
    #     logger.console('Start Suite:{}|Attributes:{}'.format(name, attrs))
