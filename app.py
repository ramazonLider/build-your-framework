from webob import Request, Response
from parse import parse
import inspect
import requests
import wsgiadapter


class SimpleFrame:
    def __init__(self) -> None:
        self.routes = dict()

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = Response()

        response = self.handle_request(request)

        return response(environ, start_response)
    
    def handle_request(self, request):
        response = Response()
        handler, kwargs = self.find_handler(request)
        
        if handler is not None:
            if inspect.isclass(handler):
                handler = getattr(handler(), request.method.lower(), None)
                if handler is None:
                    response.status_code = 405
                    response.text = "Method Not Allowed"
                    return response
                
            handler(request, response, **kwargs)
        else:
            self.default_response(response)
        return response
    
    def find_handler(self, request):
        for path, handler in self.routes.items():
            parse_result = parse(path, request.path)
            

            if parse_result is not None:
                return handler, parse_result.named
        return None, None

    def default_response(self, response):
        response.status_code = 404
        response.text = "Page not found"

    def add_route(self, path, handler):
        assert path not in self.routes, "Duplicate route, change url"
        self.routes[path] = handler

    def route(self, path):
        
        assert path not in self.routes, "Duplicate route, change url"
        
        def wrapper(handler):
            self.routes[path] = handler
            return handler
        return wrapper
    
    def test_session(self):
        session = requests.Session()
        session.mount('http://testserver', wsgiadapter.WSGIAdapter(self))
        
        return session
    
    