import kasabake
import os

from file_installer import FileInstaller
from kasabake import KasabakeCommandPlugin, NullCommandParser

PLUGIN_COMMAND = "garaemon-shell-rc-files"
PLUGIN_DIR = os.path.dirname(os.path.abspath(__file__))

class GaraemonShellRCFiles(FileInstaller):
    "install garaemon's shell setting files"
    def __init__(self, manager):
        parser = NullCommandParser(prog = PLUGIN_COMMAND,
                                   description = self.__doc__)
        parser.add_command(callback = self.callback)
        FileInstaller.__init__(self, manager,
                               PLUGIN_COMMAND,
                               parser,
                               PLUGIN_DIR)
        return
    def callback(self, options):
        files = ["zshrc", "zshrc.darwin", "zshrc.linux",
                 "bashrc", "bashrc.linux"]
        copy_dict = dict([[os.path.join(self.getPluginPath(), f),
                           os.path.join(os.path.expanduser("~"), "." + f)]
                          for f in files])
        self.installFiles(copy_dict)
        return True
    
