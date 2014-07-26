from wsgiref.simple_server import make_server
import pprint
import urlparse
from named_entity import *

def simple_app(environ, start_response):
    """Simplest possible application object"""
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    ret = ['Hello world!']
    if 'ner' in environ['PATH_INFO']:
        query = urlparse.parse_qs(environ['QUERY_STRING'])
        if 'text' in query:
            ret.append(do_ner(query['text'][0]))
    else:
        ret.append("query "+environ['QUERY_STRING'])
        ret.append("path "+environ['PATH_INFO'])
#    ret.append(pprint.pformat(environ))
    return ["\n\n".join(ret)]

httpd = make_server('', 80, simple_app)
print "Serving HTTP on port 8000..."

# Respond to requests until process is killed
httpd.serve_forever()
