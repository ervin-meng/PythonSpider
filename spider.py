# -*- coding=UTF-8 -*-
import time,json,requests,re
from Utils.Hook import Hook
from Utils.UserAgent import UserAgent
from Multiprocess.Process import Process
from Proxy.Proxy import Proxy
from Container.Collection import Collection
from Container.LineList import LineList
from Exception.SpiderException import SpiderException

class Spider:

    name = ''
    maxnum = 5
    interval = 5
    logfile = 'exception.log'

    _seeds = []
    _options = {'timeout':5,'proxy':False,'headers':{'User-Agent':'pc'}}
    _patterns = []
    _params = []
    _content = ''
    _downloading = {}
    _crawlCollection = ''
    _discoverList = ''
    _process = None
    _proxy = None
    
    def getWorkId(self):
        if isinstance(self._process,Process):
            id = self._process._pid
        else:
            id = 0
        return id
    
    def getParams(self):
        return self._params

    def getContent(self):
        return self._content

    def loadConfig(self):
        pass

    def initDiscover(self):
        self._discoverList = LineList('SpiderDiscover','redis')
        self._crawlCollection = Collection('SpiderCrawl','redis')
        self._discoverList.clean()

        for seed in self._seeds:
            self._discoverList.add(seed)
            self._crawlCollection.delete(seed)

    def __init__(self,seeds,options={},patterns=[]):
	for seed in seeds:
            if isinstance(seed,str):
                seed = {'method':'get','url':seed,'options':{}}
            self._seeds.append(seed)
        self._options.update(options)
        self._patterns = patterns
        Hook.register('onStart',self.initDiscover)

    def exe(self,workers=0):
        if workers>0:
            self._process = Process('PySpider')
            self._process.run([self.run],workers)
        else:
            Hook.invoke('onStart')
            self.run()
            Hook.invoke('onStop')

    def run(self):
        if not isinstance(self._proxy,Proxy):
            self._proxy = Proxy()
        while self._discoverList.llen()>0:
            Hook.invoke('beforeCrawl')
            self.crawl()
            Hook.invoke('afterCrawl')
            self.discover()
            Hook.invoke('afterDiscover')
            time.sleep(self.interval)
    
    def crawl(self):
        if self.maxnum > 0 and self._crawlCollection.clen() >= self.maxnum:
            raise SpiderException("[PID:%d] The crawl set more than maxnum" % self.getWorkerId())
        while True:
            if self._discoverList.llen()==0:
                raise SpiderException("[PID:%d] The discover list is empty" % self.getWorkerId())  
            self._downloading = eval(self._discoverList.get())
            if self._downloading['url'].strip() and (not self._crawlCollection.isMember(self._downloading)):
                break

        url = self._downloading['url']
        method = 'get' if self._downloading['method'].strip()=='' else self._downloading['method']
        options = self._options
        options.update(self._downloading['options'])

        self._params = {'method':method,'url':url,'options':options}

        timeout = options['timeout']
        print type(UserAgent.rand(options['headers']['User-Agent'])),UserAgent.rand(options['headers']['User-Agent'])
        if 'headers' in options:
            if 'User-Agent' in options['headers'] and options['headers']['User-Agent'].strip()!='':
                options['headers']['User-Agent'] = UserAgent.rand(options['headers']['User-Agent'])
            headers = options['headers']
        else:
            headers = {}

        if 'proxy' in options and options['proxy']==True:
            if strpos(self._downloading['url'],'https'):
                proxies = {'https':self._proxy.get(True)}
            else:
                proxies = {'http':self._proxy.get(False)}
        elif 'proxy' in options and options['proxy']!='':
            proxies = options['proxy']
        else:
            proxies = {}

        r = requests.get(url,timeout = timeout,headers = headers,proxies = proxies)
        self._content = r.text         
        self._crawlCollection.add(self._downloading)

    def discover(self):
        urls = HtmlParser.load(self._content).findText('//a/@href')
        urls = Format.url(urls,self._downloading['url'])
        urls = set(urls)

        method = self._downloading['method'] if self._downloading['method'] else ''
        options = self._downloading['options'] if self._downloading['options'] else {}

        for url in urls:
            seed = {'url':url,'method':method,'options':options}
            if self._crawlCollection.isMember(seed):
                continue
            if self._partterns:
                for parttern in self.patterns: 
                    if re.match(pattern,url): 
                        self._discoverList.add(seed)
            else:
                self._discoverList.add(seed)
        
