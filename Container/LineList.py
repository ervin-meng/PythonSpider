# -*- coding=UTF-8 -*-
import redis
    
class LineList:

    _type = 'stack' #queue
    _name = ''
    _media = ''

    def __init__(self,name='',media='redis'):
        self._name = name
        if media=='redis':
            self._media = redis.Redis(host='127.0.0.1',port=6379,decode_responses=True)

    def add(self,data):
        return self._media.rpush(self._name,data)

    def get(self):
        if(self._type=='queue'):
            return  self._media.lpop(self._name)
        else:
            return  self._media.rpop(self._name)

    def llen(self):
        return self._media.llen(self._name)

    def clean(self):
        return self._media.delete(self._name)