# -*- coding=UTF-8 -*-
import sys
sys.path.append("..")
from Container import Collection

Class Proxy:

    _config = {}
    _source = {}

    _client = None
    _httpPool = None
    _httpsPool = None

    _verifyUrl = {'http':'http://blog.jobbole.com/all-posts/','https':'https://tech.meituan.com/'}

    def __init__(self):
        self._config = include __DIR__.'/../Config.php'
        self._initPools()

    def _initPools(self):
        self._httpPool = Collection('HttpProxy','redis',self._config['redis'])
        self._httpsPool =Collection('HttpsProxy','redis',self._config['redis'])

    def get(self,https=False):
        poll = self._httpsPool if https else self._httpPool
        while True:
            ip = poll.get(https)
            if ip && self.verify(ip,https):
                break
        if (not ip) && (not https):
            ip = self.get(True)
        return ip

    def add(self,ip,https=False):
        pool = self._httpsPool if https else self._httpPool
        return pool.add(ip);

    def rem(self,ip,https=False):
        pool = self._httpsPool if https else self._httpPool
        return pool.delete(ip);

    def verify(self,ip,https=False):
        if self_client== None:
            self._client = Client()
        
        verifyUrl = self._verifyUrl['https'] if https else self._verifyUrl['http']

        try: 
            self._client->request('get',$verifyUrl,['proxy'=>$ip,'timeout'=>5,'verify'=>False])
            return True
        except: Exception,e
            self.rem(ip,https)
            return False

    def registerSourceHandler(self,source,func=''):
        if func=='' && isintance(source,list):
            for classname in source
                self._source[classame] = classame();
        else:
            self._source[source] = func;
        
    def scanFromSource(self,source='',process=False):           
        if Source=='':
            if process:
                process = Process(process);
                for source in self._source:
                    jobs [] = self._scanFromSource(source)
                process.run(jobs,1);
            else:
                for source in self._source:
                    self._scanFromSource($source)
        elif source in self._source:
            if process:
                self._initPools()
            ips = self._source[source]()
            if ips:
                for ip in ips
                    if self._verify(ip['ip'],ip['https']):
                        self,add(ip['ip'],ip['https'])
        else:
            return False