## dispatch

import glob
import os
import config

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
        elif len(self.params) == 2 and self.params[1] == "help":
            self.usage()
        elif len(self.params) == 3 and self.params[1] == "help":
            app = self.findapp(self.params[2])
            if app == None:
                print "Can't find %s to usaged\n" % self.params[2]
                print "Try to run '%s help' to get help\n" % self.entryname
            else:
                #print app
                cmdline = "%s %s" % (" ".join(app), "help")
                print "cmdline: %s\n" % cmdline
                os.system(cmdline)
        else:
            if len(self.params) >= 4:
                print "4\n"
                self.cmd = "%s-%s-%s" % (self.params[1], self.params[2], self.params[3])
                self.args = " ".join(self.params[4:])
            elif len(self.params) >= 3:
                print "3\n"
                self.cmd = "%s-%s" % (self.params[1], self.params[2])
                self.args = " ".join(self.params[3:])
            elif len(self.params) >= 2:
                print "1\n"
                self.cmd = "%s" % (self.params[1])
                self.args = " ".join(self.params[2:])
            else:
                pass

            print "cmd: %s  <=> %s\n" % (self.cmd, self.args)
                
            app = self.findapp(self.cmd)
            if app == None:
                print "Can't find %s to usaged\n" % self.cmd
                print "Try to run '%s help' to get help\n" % self.entryname
            else:
                #print app
                cmdline = "%s %s" % (" ".join(app), self.args)
                print "cmdline: %s\n" % cmdline
                os.system(cmdline)

        
    def usage(self):
        print "Use: %s help" % self.entryname
        for app in self.appmap:
            print "Use: %s %s [argv]" % (self.entryname, app)

        print "Use: %s help <app>" % self.entryname
        
    def findapp(self, app):
        if app in self.appmap:
            return self.appmap[app]
        else:
            return None
        
    def getappmap(self):
        appdir = "%s/%s" % (self.srcdir, config.appdirname)
        applist = []
        for appcfgitem in config.appnames.keys():
            applist += glob.glob(appdir + "/" + appcfgitem)

        applist = map(lambda x: os.path.basename(x), applist)
        for ignore in config.appignorefiles:
            try:
                applist.remove(ignore)
            except:
                pass

        for app in applist:
            appinfo = []
            appname, appext = os.path.splitext(app)

            ## for command line
            appinfo.append(config.appnames["*" + appext])
            appinfo.append(self.srcdir + "/" + config.appdirname + "/" + app)
            self.appmap[appname] = appinfo
        #print self.appmap
