# -*- coding=UTF-8 -*-
import urlparse,re

class Format:

    @staticmethod
    def url(urls,benchmark):
    
        parsed = urlparse.urlparse(benchmark)
        siteurl = parsed.scheme+'://'+parsed.netloc
        
        formaturls = []

        for url in urls:
            if not url:
                continue

            if not re.match("^(?:http)s?://",url,re.IGNORECASE): 
                if (url[0] == '/') or (url[:2] == './') or (url[:3] == '../'):
                    url = siteurl+Format.path(url,parsed.path)
                else:
                    continue;

            formaturls.append(url)

        return formaturls
        
    @staticmethod
    def path(path,cwd='',separator='/'):

        cwd = cwd if cwd else os.path.abspath('.')

        if path[:2] == '.'+separator:
            path = cwd+path[1:]
        elif path[:3] =='..'+separator:
            while True:
                path = path[:3]
                if cwd:
                    cwd = os.path.dirname(cwd)
                if path[:3] != '..'+separator:
                    break

            path = separator+path if cwd == os.path.sep else cwd+separator+path

        return path