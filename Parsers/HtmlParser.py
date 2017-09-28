# -*- coding=UTF-8 -*-
import os
from lxml import etree
from Adapters.CssSelector import CssSelector

class HtmlParser:

    _contextnode = None
    _root = None
    
    @classmethod
    def load(cls,html):
        if os.path.isfile(html):
            with open(html,'r') as f:
                html = f.read()
                
        contextnode = etree.HTML(html)
        cls._root = contextnode
 
        return HtmlParser(contextnode)

    def __init__(self,contextnode = None): 
        self._contextnode = contextnode

    def findText(self,expression,contextnode = None):
        expression = CssSelector.translate(expression)
        text = [];
        nodeList = self.xpath(expression,contextnode)
        for node in nodeList:
            if isinstance(node,HtmlParser):
                text.append(node.text())
            else:
                text.append(node)
        return text

    def find(self,expression,contextnode = None):
        expression = CssSelector.ranslate(expression)
        return self.xpath(expression,contextnode)

    def xpath(self,expression,contextnode = None):
        if contextnode is None and self._contextnode is not None:
            contextnode = self._contextnode

        nodeList = contextnode.xpath(expression)
  
        result = []
        for node in nodeList:
            node = HtmlParser(node) if isinstance(node,etree._Element) else node
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
        contextnode =  contextnode if contextnode is not None else self._contextnode
        return etree.tostring(contextnode)

    def text(self,contextnode = None):
        contextnode =  contextnode if contextnode else self._contextnode
        return contextnode.text