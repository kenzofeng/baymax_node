import logging
import os
import tempfile


class TestListener:
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        self.logger = logging.getLogger('listern')
        rf = logging.FileHandler(os.path.join(tempfile.gettempdir(), 'listener.txt'))
        self.logger.setLevel(logging.INFO)
        self.logger.addFilter(rf)
        self.logger.info('111111111111111111')

    def start_keyword(self, name, attrs):
        self.logger.info("%s '%s'\n" % (name, attrs['args']))

    def end_keyword(self, name, attrs):
        self.logger.info("%s '%s'\n" % (name, attrs['args']))

    def start_suite(self, name, attrs):
        self.logger.info("%s '%s'\n" % (name, attrs['doc']))

    def start_test(self, name, attrs):
        tags = ' '.join(attrs['tags'])
        self.logger.info("- %s '%s' [ %s ] :: " % (name, attrs['doc'], tags))

    def end_test(self, name, attrs):
        if attrs['status'] == 'PASS':
            self.logger.info('PASS\n')
        else:
            self.logger.info('FAIL: %s\n' % attrs['message'])

    def end_suite(self, name, attrs):
        self.logger.info('%s\n%s\n' % (attrs['status'], attrs['message']))
