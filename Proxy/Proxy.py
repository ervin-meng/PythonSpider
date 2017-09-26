# -*- coding=UTF-8 -*-
import sys,requests
sys.path.append("..")
from Container.Collection import Collection

class Proxy:

    _source = {}

    _httpPool = None
    _httpsPool = None
    _verifyUrl = {'http':'http://blog.jobbole.com/all-posts/','https':'https://tech.meituan.com/'}

    def __init__(self):
        self._initPools()

    def _initPools(self):
        self._httpPool = Collection('HttpProxy','redis')
        self._httpsPool = Collection('HttpsProxy','redis')

    def get(self,https=False):
        poll = self._httpsPool if https else self._httpPool
        while True:
            ip = poll.get(https)
            if ip and self.verify(ip,https):
                break
        if (not ip) and (not https):
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

        if https:
            verifyUrl = self._verifyUrl['https']
            proxies = {'https':ip}
        else:
            verifyUrl = self._verifyUrl['http']
            proxies = {'http':ip}

        try: 
            r = requests.get(verifyUrl,timeout = 5,proxies = proxies)
            return True
        except Exception,e:
            self.rem(ip,https)
            return False

    def registerSourceHandler(self,source,func=''):
        if func=='' and isintance(source,list):
            for classname in source:
                self._source[classame] = classame();
        else:
            self._source[source] = func;
        
    def scanFromSource(self,source='',process=False):           
        if Source=='':
            if process:
                process = Process(process);
                job = []
                for source in self._source:
                    jobs.append(self._scanFromSource)
                process.run(jobs,1)
            else:
                for source in self._source:
                    self._scanFromSource(source)
        elif source in self._source:
            if process:
                self._initPools()
            ips = self._source[source]()
            if ips:
                for ip in ips:
                    if self._verify(ip['ip'],ip['https']):
                        self,add(ip['ip'],ip['https'])
        else:
            return False