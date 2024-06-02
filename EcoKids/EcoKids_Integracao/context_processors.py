# context_processors.py

def csp_nonce(request):
    return {'nonce': getattr(request, 'nonce', '')}
