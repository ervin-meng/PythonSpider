# -*- coding=UTF-8 -*-
import lxml.etree,os
from Adapters.CssSelector import CssSelector

class HtmlParser:

    _contextnode = None
    _root = None
    
    @classmethod
    def load(cls,html):
        if os.is_file(html):
            with open(html,'r') as f:
                html = f.read()
                
        contextnode = etree.HTML(html.decode('utf-8'))
        cls._root = contextnode
 
        return HtmlParser(contextnode)

    def __init__(self,contextnode = None): 
        self._contextnode = contextnode

    def findText(self,expression,contextnode = None):
        expression = CssSelector.translate(expression)
        text = [];
        nodeList = self.xpath(expression,contextnode)
        for node in nodeList:
            text.append(node.text)
        return text

    def find(self,expression,contextnode = None):
        expression = CssSelector.ranslate(expression)
        return self.xpath(expression,contextnode)

    def xpath(self,expression,contextnode = None):
        if not contextnode and self._contextnode:
            contextnode = self._contextnode

        nodeList = contextnode.xpath(expression)
        result = []
        for node in nodeList:
            node = HtmlParser(node)
            result.append(node)
            
        return result

    def remove(self,expression,contextnode = None):
        if not contextnode and self._contextnode:
            contextnode = self._contextnode

        expression = CssSelector.translate(expression)
        nodeList = contextnode.xpath(expression)
        for node in nodeList:
            node.getparent().remove(node)

        return self

    def html(self,contextnode = None):
        contextnode =  contextnode if contextnode else self._contextnode
        return etree.tostring(contextnode)

    def text(self,contextnode = None):
        contextnode =  contextnode if contextnode else self._contextnode
        return contextnode->text