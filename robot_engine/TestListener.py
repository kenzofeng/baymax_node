from robot.api import logger


class TestListener:
    ROBOT_LISTENER_API_VERSION = 2
    def __init__(self):
        logger.info('111111111111111')

    def start_keyword(self, name, attrs):
        logger.info("%s '%s'\n" % (name, attrs['args']))

    def end_keyword(self, name, attrs):
        logger.info("%s '%s'\n" % (name, attrs['args']))

    def start_suite(self, name, attrs):
        logger.info("%s '%s'\n" % (name, attrs['doc']))

    def start_test(self, name, attrs):
        tags = ' '.join(attrs['tags'])
        logger.info("- %s '%s' [ %s ] :: " % (name, attrs['doc'], tags))

    def end_test(self, name, attrs):
        if attrs['status'] == 'PASS':
            logger.info('PASS\n')
        else:
            logger.info('FAIL: %s\n' % attrs['message'])

    def end_suite(self, name, attrs):
        logger.info('%s\n%s\n' % (attrs['status'], attrs['message']))
