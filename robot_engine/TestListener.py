from robot.api import logger


class TestListener:
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        logger.console('Hello, world!')

    def start_keyword(self, name, attrs):
        logger.console("%s '%s'\n" % (name, attrs['args']))

    def end_keyword(self, name, attrs):
        logger.console("%s '%s'\n" % (name, attrs['args']))

    def start_suite(self, name, attrs):
        logger.console("%s '%s'\n" % (name, attrs['doc']))

    def start_test(self, name, attrs):
        tags = ' '.join(attrs['tags'])
        logger.console("- %s '%s' [ %s ] :: " % (name, attrs['doc'], tags))

        # def end_test(self, name, attrs):
        #     if attrs['status'] == 'PASS':
        #         self.logger.info('PASS\n')
        #     else:
        #         self.logger.info('FAIL: %s\n' % attrs['message'])

    def end_suite(self, name, attrs):
        logger.console('%s\n%s\n' % (attrs['status'], attrs['message']))
