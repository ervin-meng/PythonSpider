# -*- coding=UTF-8 -*-
import redis

class Collection:

    _name = ''
    _media = ''

    def __init__(self,name,media='redis'): 
        self._name = name
        if media=='redis':
            self._media = redis.Redis(host='127.0.0.1',port=6379,decode_responses=True)

    def add(self,data):
        return self._media.sadd(self._name,data)

    def delete(self,data):
        return self._media.srem(self._name,data)

    def get(self,pop=True):
        if pop:
            return self._media.spop(self._name)
        else:
            return self._media.srandmember(self._name)

    def isMember(self,data):
        return self._media.sismember(self._name,data)

    def clen(self):
        return self._media.scard(self._name)

    def clean(self):
        return self._media.delete(self._name)