from pulsar.async import MainIOLoop

from .std import HttpClient1, urlencode, getproxies_environment

HttpClients={1:HttpClient1}
try:
    from ._httplib2 import HttpClient2
    HttpClients[2] = HttpClient2
except ImportError:
    pass


form_headers = {'Content-type': 'application/x-www-form-urlencoded'}


class AsyncHttpClient(object):
    
    def __init__(self, c, ioloop = None):
        self.client = c
        self.ioloop = ioloop or MainIOLoop.instance()
        
    def request(self, *args, **kwargs):
        return self.ioloop.add_callback(
            lambda : self.client.request(*args, **kwargs)
        )
        
        


def HttpClient(cache = None, proxy_info = None,
               timeout = None, type = 1, ioloop = None,
               async = False):
    '''Create a http client handler using different implementation.
It can build a synchronous or an asyncronous handler build on top
of the :class:`pulsar.IOLoop`. 
    
:parameter cache: Cache file. Default ``None``.
:parameter proxy_info: Dictionary of proxies. Default ``None``.
:parameter timeout: Connection timeout. Default ``None``.
:parameter type: Handler implementation. Default ``1``.
:parameter async: Synchronous or Asynchronous. Default ``False``.
'''
    if type not in HttpClients:
        raise ValueError('HttpClient{0} not available'.format(type))
    client = HttpClients[type]
    proxy = proxy_info
    if proxy is None:
        proxy = getproxies_environment()
        
    c = client(proxy_info = proxy, cache = cache, timeout = timeout)
    if async:
        return AsyncHttpClient(c, ioloop = ioloop)
    else:
        return c

    
