# -*- coding=UTF-8 -*-
import os,sys,signal,time
sys.path.append("..")
from Utils.Hook import Hook
from setproctitle import *

class Process:

    _STATUS = 0  #0 初始值 1 开始 2 运行中 3 结束
    _name = ''
    _pid = 0
    _ppid = 0
    _pidfile = ''
    _stdoutfile = ''
    _workers = {}
    _commands = ['start','stop','restart','reload','help']
    _option = False
    _count = 0
    _jobs = []

    def run(self,jobs,count=1):
        if(count<1):
           exit('The number of worker processes must be greater than one')

        self._count = count
        self._jobs = jobs
        argc = len(sys.argv)

        if argc>2:
            self._option = sys.argv[2]

        if argc>1 and sys.argv[1] in self._commands:
            eval('self._'+sys.argv[1]+'()')
        else:
            self._help()

    def _start(self):
        if os.path.exists(self._pidfile):
            exit("Process "+self._name+" is Running")

        if self._option == '-d':
            self._daemonize()

        self.log("master process [PID:%d] started" % os.getpid())
        self._STATUS = 1;
        Hook.invoke('onStart')
        self._registerSignal()

        for job in self._jobs:
            self._forkWorkers(job,self._count)

        self._createMasterPidFile()
        self._listen()

    def _stop(self):
        Hook.invoke('onStop')
        os.kill(self.getMasterPid(),signal.SIGINT);

    def _restart(self):
        if not os.path.exists(self._pidfile):
            exit("The process "+self._name+" is not Running")

        Hook.invoke('onRestart')
        os.kill(self.getMasterPid(),signal.SIGINT)

        print "The process %s is restarting" % self._name

        while os.path.exists(self._pidfile):
            time.sleep(1)

        self._start()

    def _reload(self):
        if not os.path.exists(self._pidfile):
            exit("The process "+self._name+" is not Running")

        Hook.invoke('onReload')
        os.kill(self.getMasterPid(),signal.SIGUSR1)
        self._start()

    def _help(self):
        msg='''
USAGE
  yourfile.php command [options]
COMMANDS
  help         Show this help.
  restart      Stop all running process, then Start.
  start        Start process.
  stop         Stop all running process.
  reload       Gracefully restart daemon processes in-place to pick up changes to
               source. This will not disrupt running workers. most publishing should use yourfile.php reload
OPTIONS
  -d           Start or Reload in daemon '''
        print msg;

    def __init__(self,name='Process',pidfile='',stdoutfile=''):
        __DIR__ = os.path.dirname(os.path.realpath(__file__))
        self._name = name;
        self._pidfile = pidfile if pidfile else __DIR__+"/"+name+".pid"
        self._stdoutfile = stdoutfile if stdoutfile else __DIR__+"/"+name+"_stdout.log"

    def _registerSignal(self):
        signal.signal(signal.SIGUSR1,self.signalHandler) #reload
        signal.signal(signal.SIGINT,self.signalHandler) #stop 
        signal.signal(signal.SIGPIPE,signal.SIG_IGN)

    def signalHandler(self,signalnum,stack):
        if signalnum == signal.SIGUSR1:
            os.remove(self._pidfile)
            exit()
        elif signalnum == signal.SIGINT:
            for pid in self._workers:
                os.kill(pid,signal.SIGKILL)
                self.log("worker process [PID:%d] stoped" % pid)
                del self._workers[pid]   
            os.remove(self._pidfile)
            self.log("master process [PID:%d] stoped" % self._pid)
            exit()

    def _daemonize(self):
        os.umask(0)
        if os.fork() > 0:
            exit(0)
        os.setsid()

        if os.fork() >0: 
            exit(0)

        sys.stdout.flush()  
        sys.stderr.flush()  

        so = open(self.stdout, 'a+')  
        if self.stderr:  
            se = open(self.stderr, 'a+', 0)  
        else:  
            se = so  

        os.dup2(so.fileno(),sys.stdout.fileno())  
        os.dup2(se.fileno(),sys.stderr.fileno())  

    def _forkWorkers(self,job,count=1):
        while count >= 1:
            pid = os.fork()
            self._pid = os.getpid()

            time.sleep(1)

            if pid == 0:
                setproctitle(self._name+": worker process.")
                self.log("worker process [PID:%d] started" % self._pid)
                self._ppid = os.getppid()
                if callable(job):
                    job()
                else:
                    self.log(str(job)+' is not callalbe')
                exit(666)
            else:
                setproctitle(self._name+": master process. "+self.getRunFileName())
                self._workers[pid] = job

            count = count -1


    def _listen(self):
        self.log("master process [PID:%d] listening" % self._pid)

        self._STATUS = 2

        while True:
            pid,status = os.wait()
 
            if pid>0 and pid in self._workers.keys():  
                self.log("worker process [PID:"+str(pid)+"] stoped with [STATUS:"+str(status)+"]")

                job = self._workers[pid]
                del self._workers[pid]

                if self._STATUS!=3 and status!=39424:
                    self._forkWorkers(job)

                if len(self._workers)==0:
                    self._stop()
                    break
        while True:
            pass

    def log(self,msg,file=''):
        dt = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        print dt+" [NAME:"+self._name+"] "+msg+"\n";

    def getMasterPid(self):
        f = open(self._pidfile,'r')
        pid = f.read()
        f.close()
        return int(pid)

    def getRunFileName(self):
        return os.path.realpath(sys.argv[0])

    def _createMasterPidFile(self):
        f = open(self._pidfile,'w')
        f.write(str(self._pid))
        f.close()