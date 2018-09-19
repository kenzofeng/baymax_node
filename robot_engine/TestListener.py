import logging



class TestListener:
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        self.logger = logging.getLogger('robot')
        self.logger.debug('111111111111111111')

    def start_keyword(self, name, attrs):
        self.logger.debug("%s '%s'\n" % (name, attrs['args']))

    def end_keyword(self, name, attrs):
        self.logger.debug("%s '%s'\n" % (name, attrs['args']))

    def start_suite(self, name, attrs):
        self.logger.debug("%s '%s'\n" % (name, attrs['doc']))

    def start_test(self, name, attrs):
        tags = ' '.join(attrs['tags'])
        self.logger.debug("- %s '%s' [ %s ] :: " % (name, attrs['doc'], tags))

    def end_test(self, name, attrs):
        if attrs['status'] == 'PASS':
            self.logger.debug('PASS\n')
        else:
            self.logger.debug('FAIL: %s\n' % attrs['message'])

    def end_suite(self, name, attrs):
        self.logger.debug('%s\n%s\n' % (attrs['status'], attrs['message']))
