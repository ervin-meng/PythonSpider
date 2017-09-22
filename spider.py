# -*- coding=UTF-8 -*-
from Exception.SpiderException import SpiderException
from Multiprocess.Process import Process
from Utils.Hook import Hook
import time
import json

class Spider:

    _config= {}
    _seeds = []
    _options = {'timeout':5,'proxy':False}
    _patterns = []
    _params = []

    _content
    _downloading

    _crawlCollection;
    _discoverList;
    _process;
    _proxy;
    
    name;
    maxnum = 5
    interval = 5
    logfile = 'exception.log'

    def getWorkId(self):
        pass
    
    def getParams(self)：
        return self._params

    def getContent(self):
        reutnr self._content

    def loadConfig(self):
        pass

    def initDiscover(self):
        pass

    def __init__(self,seeds,options={},patterns=[]):
	for seed in seeds:
            if isinstance(seed,str):
                seed = {'method':'get','url':seed,'options':{}}
            self._seeds.append(seed)
        self._options.update(options)
        self._patterns = patterns

    def exec(self,workers=0):
        if workers>0:
            self._process = Process('Spider');
        else:
            Hook._invoke('onStart');
            self.run();
            Hook._invoke('onStop');

    def run(self):
        if not isinstance(self._proxy,Proxy):
            self._proxy = Proxy()
        while self._discoverList.len()>0:
            try:
                Hook._invoke('beforeCrawl')
                self.crawl()
                Hook._invoke('afterCrawl')
                self.discover()
                Hook._invoke('afterDiscover')
            except Exception,e:
                self._exceptionHandler(e);
            time.sleep(self.interval);
    
    def crawl(self):
        if self.max > 0 and self._crawlCollection.count() >= self.max:
            Raise SpiderException("[PID:"+self.getWorkerId()+"] The crawl set more than max")

        while True:
            if self._discoverList.len()==0:
                Raise SpiderException("[PID:"+self.getWorkerId()+"] The discover list is empty")          
            self._downloading = self._discoverList.next()
            self._downloading = json.loads(self._downloading)
            if not (self._crawlCollection.isMember(json.dumps(self._downloading)) or self._downloading['url'].strip()==''):
                break

        url = self._downloading['url']
        method = 'get' if self._downloading['method'].strip()=='' else self._downloading['method']
        options = self.options.update(self._downloading['options'])

        if 'headers' in options and 'User-Agent' in options['headers'] and options['headers']['User-Agent'].strip()!='':
            options['headers']['User-Agent'] = UserAgent._rand(options['headers']['User-Agent'])

        if 'proxy' in options and options['proxy']===true:
            https = True if strpos(self._downloading['url'],'https') else False
            options['proxy'] = self._proxy.get(https)

        self._params = {'method':method,'url':url,'options':options}

        $client = new GuzzleHttp\Client();
        self._content = $client->request($method,$url,$options)->getBody()->getContents()         
        self._crawlCollection.add(json.dumps(self._downloading))
        
