# dispatch.py
# -*- coding: utf-8 -*-

import os
import framework.config as config

class Dispatch:

    def __init__(self, workdir, srcdir, argv):
        self.workdir = workdir
        self.srcdir = srcdir
        self.params = argv
        self.appmap = {}
        self.entryname = os.path.basename(argv[0])

    def run(self):
        self.getappmap()
        if len(self.params) == 1:
            self.usage()
        else:
            cmd = ""
            args = ""
            app = None
            match = False

            for num in range(config.maxmatch, -1, -1):
              if len(self.params) >= num and match is False:
                cmd = "-".join(self.params[1:num-1])
                args = " ".join(self.params[num:])
                app = self.findapp(cmd)
                if app is not None:
                    match = True
                    break

            if app is None and match is False:
                print("Can't find %s to usaged\n" % cmd)
                print("Try to run '%s help' to get help\n" % self.entryname)
            else:
                if config.verbose is True:
                    print(app)

                cmdline = "%s %s" % (" ".join(app), args)
                print("cmdline: %s\n" % cmdline)
                os.system(cmdline)

    def usage(self):
        for key, value in sorted(self.appmap.items()):
            print("Use: %s %s [argv]" % (self.entryname, key.replace("-", " ")))

    def findapp(self, app):
        if app in self.appmap.keys():
            return self.appmap[app]
        else:
            return None

    def getappmap(self):
        appdir = "%s/%s" % (self.srcdir, config.appdirname)
        applist = []

        for (dirname, subdir, subfile) in os.walk(appdir):
            if config.verbose is True:
                print('Dirname: %s' % dirname)
                print('Subdir: %s' % subdir)
                print('Subfile: %s' % subfile)
            for f in subfile:
                filefullname = "%s/%s" % (dirname, f)
                if os.access(filefullname, os.X_OK):
                    applist.append(f)
            break

        for ignore in config.appignorefiles:
            try:
                applist.remove(ignore)
            except Exception:
                pass

        for app in applist:
            appinfo = []
            appname, appext = os.path.splitext(app)

            if appext == "":
                appinfo.append("")
            elif appext in config.appnames:
                appinfo.append(config.appnames[appext])
            else:
                continue

            appinfo.append(self.srcdir + "/" + config.appdirname + "/" + app)
            self.appmap[appname] = appinfo

        if config.verbose is True:
            print(self.appmap)
