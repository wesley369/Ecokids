import os
from django.utils.deprecation import MiddlewareMixin

class CSPNonceMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.nonce = os.urandom(16).hex()
        response = self.get_response(request)
        if 'Content-Security-Policy' not in response:
            response['Content-Security-Policy'] = (
                "default-src 'self'; "
                f"script-src 'self' 'nonce-{request.nonce}'; "
                "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
                "font-src 'self' https://fonts.gstatic.com; "
                "img-src 'self' data:; "
                "connect-src 'self' https://ka-f.fontawesome.com;"
            )
        return response

    def process_template_response(self, request, response):
        response.context_data['nonce'] = request.nonce
        return response


class RemoveServerHeaderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        del response['Server']
        return response
