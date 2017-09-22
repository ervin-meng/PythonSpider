# -*- coding=UTF-8 -*-
import os,sys,signal,datetime
sys.path.append("..")
from Utils import Hook

    class Process:
        
        _STATUS = 0;  //0 初始值 1 开始 2 运行中 3 结束
        
        _name
        _pid
        _ppid = 0
        
        _pidfile;
        _stdoutfile;

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
            
            if sys.argv.count()>2:
                $this->_option = $argv[2]
            
            if sys.argv.count()>1 and argv[1] in self._commands:
                self.'_'+sys.argv[1]()
            else:
                self._help()

        def _start(self):
            if os.path.exists(self._pidfile):
                exit("Process "+self._name+" is Running")
            
            if self._option == '-d':
                self._daemonize()
                
            self.log("master process [PID:"+os.getpid()+"] started")
            self._STATUS = 1;
            Hook._invoke('onStart')
            self._registerSignal()
            
            for job in self._jobs:
                self._forkWorkers(job,self._count)

            self._createMasterPidFile()
            self._listen()
                          
        def _stop(self):
            Hook._invoke('onStop')
            os.kill(self.getMasterPid(),signal.SIGINT);

        def _restart(self):
            if not os.path.exists(self._pidfile):
                exit("The process "+self._name+" is not Running")
            
            Hook._invoke('onRestart')
            os.kill(self.getMasterPid(),signal.SIGINT)
            
            print "The process %s is restarting" % self._name
            
            while os.path.exists(self._pidfile):
                time.sleep(1)

            self._start()
        
        def _reload(self):
            if not os.path.exists(self._pidfile):
                exit("The process "+self._name+" is not Running")
            
            Hook._invoke('onReload')
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
            self._pidfile = pidfile if pidfile else __DIR__+"/"+name.".pid"
            self._stdoutfile = stdoutfile if stdoutfile else __DIR__+"/"+name."_stdout.log"
      
        def _registerSignal(self):
            signal.signal(signal.SIGUSR1,slef.signalHandler) #reload
            signal.signal(signal.SIGINT,self.signalHandler) #stop 
            signal.signal(signal.SIGPIPE,signal.SIG_IGN)
            
        def signalHandler(signalnum,stack):
            if signalnum == signal.SIGUSR1: #reload
                os.remove(self._pidfile)
                exit()
            elif signalnum == signal.SIGINT: #stop
                self._STATUS = 3;
                
                for pid in self._workers
                    os.kill(pid,signal.SIGKILL)
                    self.log("worker process [PID:"+pid+"] stoped")
                    del self._workers[pid]   
                os.remove(self._pidfile)
                self.log("master process [PID:"+self._pid+"] stoped")
                exit();
        
        protected  function _daemonize()
        {
            umask(0);
            
            $pid = pcntl_fork();
            
            if (-1 === $pid) 
            {
                exit('daemonize fork fail');
            } 
            elseif ($pid > 0) {
                exit(0);
            }
            
            if (-1 === posix_setsid())
            {
                exit("daemonize setsid fail");
            }
            
            $pid = pcntl_fork();
            
            if (-1 === $pid) 
            {
                exit("daemonize fork fail again");
            } 
            elseif (0 !== $pid) 
            {
                exit(0);
            }
            
            if (fopen($this->_stdoutfile, "a")) 
            {
                global $STDOUT, $STDERR;
                unset($handle);
                @fclose(STDOUT);
                @fclose(STDERR);
                $STDOUT = fopen($this->_stdoutfile,"a");
                $STDERR = fopen($this->_stdoutfile,"a");
            } 
            else {
                exit('daemonize can not open stdoutFile ' .$this->_stdoutfile);
            }
        }
        
        protected function _forkWorkers($job,$count=1)
        {
            while($count>=1)
            {
                $pid = pcntl_fork();
                $this->_pid = posix_getpid();
                
                sleep(1);
                
                switch($pid)
                {
                    case '-1':
                        exit('can not fork child process ');
                    break;

                    case '0';
                        $this->_setProcessTitle("{$this->_name}: worker process.");
                        $this->log("worker process [PID:{$this->_pid}] started");
                        $this->_ppid = posix_getppid();
                        call_user_func_array($job,[]);
                        exit(666);
                    break;

                    default:
                        $this->_setProcessTitle("{$this->_name}: master process. ".$this->getRunFileName());
                        $this->_workers[$pid] = $job;
                    break;
                }
                
                $count--;
            }
        }
        
        protected function _listen()
        {
            $this->log("master process [PID:{$this->_pid}] listening");
            
            self::$_STATUS = 2;
            
            while (1) 
            {
                pcntl_signal_dispatch();
                $pid = pcntl_wait($status);
                
                if($pid>0 && isset($this->_workers[$pid]))
                {   
                    $this->log("worker process [PID:{$pid}] stoped with [STATUS:{$status}]");
                  
                    $job = $this->_workers[$pid];
                    unset($this->_workers[$pid]);
                    
                    if(self::$_STATUS!=3 && $status!=39424)
                    {
                        $this->_forkWorkers($job);
                    }
                    
                    if(empty($this->_workers))
                    {
                        $this->_stop();
                    }
                }
            }
        }
        
        def log(self,msg,file=''):
            datetime = datetime.datetime.strptime(string,'%Y-%m-%d %H:%M:%S')
            print datetime+" [NAME:"+self._name+"] "+msg+"\n";
         
        def getMasterPid(self):
            return open(self._pidfile,'r').read()

        def getRunFileName(self):
            return os.path.realpath(sys.argv[0])
                        
        def _createMasterPidFile(self):
            return open(self._pidfile,'w').write(self._pid)
        
        
        protected function _setProcessTitle($title)
        {
            cli_set_process_title($title);
        }
