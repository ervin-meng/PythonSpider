# -*- coding=UTF-8 -*-

class Hook:

    _events = {}
    
    @classmethod
    def register(cls,event,action,params=''):
        if event not in cls._events:
            cls._events[event] = []
        if callable(action):
	    cls._events[event].append([action,params]);
            
    @classmethod
    def invoke(cls,event):
        hooks = cls._events[event] if event in cls._events else []
        for hook in hooks:
            hook()


    
        
