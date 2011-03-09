import kasabake
import os

import twitter

from file_installer import FileInstaller
from kasabake import KasabakeCommandPlugin, CommandParser

PLUGIN_COMMAND = "garaemon-screen"
PLUGIN_DIR = os.path.dirname(os.path.abspath(__file__))

class GaraemonScreen(FileInstaller):
    "install garaemon's screen setting files"
    def __init__(self, manager):
        parser = CommandParser(prog = PLUGIN_COMMAND,
                               description = self.__doc__)
        parser.add_command("install",
                           narg = 0,
                           callback = self.install,
                           help = "install screen setting files")
        parser.add_command("twitter",
                           narg = 0,
                           callback = self.twitter,
                           help = "print timeline of your twitter.")
        FileInstaller.__init__(self, manager,
                               PLUGIN_COMMAND,
                               parser,
                               PLUGIN_DIR)
        return
    def install(self, options):
        files = ["screenrc", "screenrc.defaults", "screenrc.leaf"]
        copy_dict = dict([[os.path.join(self.getPluginPath(), f),
                           os.path.join(os.path.expanduser("~"), "." + f)]
                          for f in files])
        self.installFiles(copy_dict)
        p = self.getManager().getPlugin("easy_install")
        p.installPackages(options, "tweepy")
        return True
    def twitter(self, options):
        twitter.main()
        return True
    
