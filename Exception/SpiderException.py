# -*- coding=UTF-8 -*-
class SpiderException(Exception):
    def __init__(self,msg):
	Exception.__init__(self)  
        self.msg = msg
