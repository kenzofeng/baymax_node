from robot.output import LOGGER
from robot.output.loggerhelper import Message


class TestListener:
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        LOGGER.log_message(Message('Hello, world!', 'INFO'))

    def start_keyword(self, name, attrs):
        LOGGER.log_message(Message("%s '%s'\n" % (name, attrs['args']), 'INFO'))

    def end_keyword(self, name, attrs):
        LOGGER.log_message(Message("%s '%s'\n" % (name, attrs['args']), 'INFO'))

    def start_suite(self, name, attrs):
        LOGGER.log_message(Message("%s '%s'\n" % (name, attrs['doc']), 'INFO'))

    def start_test(self, name, attrs):
        tags = ' '.join(attrs['tags'])
        LOGGER.log_message(Message("- %s '%s' [ %s ] :: " % (name, attrs['doc'], tags), 'INFO'))

        # def end_test(self, name, attrs):
        #     if attrs['status'] == 'PASS':
        #         self.logger.info('PASS\n')
        #     else:
        #         self.logger.info('FAIL: %s\n' % attrs['message'])

    def end_suite(self, name, attrs):
        LOGGER.log_message(Message('%s\n%s\n' % (attrs['status'], attrs['message']), 'INFO'))
