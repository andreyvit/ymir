""" ymir.bin._ymir
"""
import os

import fabric

from goulash.settings import Settings as BaseSettings
from goulash.settings import GoulashConfigParser
from goulash.settings import SettingsError

CMD_INIT = 'init'
COMMANDS = [
    CMD_INIT,
    'create_bucket']
from ymir.version import __version__
from ymir.base import Reporter

class InitCmd(Reporter):
    def __call__(self, target):
        target = os.path.abspath(os.path.expanduser(target))
        if os.path.exists(target):
            self.report(
                'cannot initialize ymir for a directory '
                'that already exists: {0}'.format(target))
        else:
            self.report('initializing new project', target)
            ymir_bin = os.path.dirname(__file__)
            ymir = os.path.dirname(ymir_bin)
            example_fabfile = os.path.join(ymir, 'fabfile.py')
            assert os.path.exists(example_fabfile)
            
init_cmd = InitCmd()

class Settings(BaseSettings):

    environ_key  = 'YMIR_SETTINGS'
    default_file = 'ymir.ini'

    def load(self, file, config={}):
        """ returns a dictionary with key's of the form
            <section>.<option> and the values
        """
        config = config.copy()
        cp = GoulashConfigParser()
        return cp._sections

    def run(self):
        super(Settings,self).run()
        command = self.args.command
        target = self.args.target
        if command not in COMMANDS:
            err = "error: '{0}' is not a valid command (choose from: {1})"
            err = err.format(command, '{' + ' | '.join(COMMANDS) + '}')
            raise SystemExit(err)
        if command == CMD_INIT:
            init_cmd(target)

    def show_version(self):
        """ subclassers should call super
            and then print their own junk """
        print 'ymir=={0}'.format(__version__)

    def get_parser(self):
        """ build the default parser """
        parser = super(Settings, self).get_parser()
        parser.add_argument('command', nargs='?',)
        parser.add_argument('target', nargs='?', default='.')
        return parser


def entry(settings=None):
    """ Main entry point """
    #from ymir import settings
    settings = settings or Settings()
    settings.run()

if __name__=='__main__':
    entry()
