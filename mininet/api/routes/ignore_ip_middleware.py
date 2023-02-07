BLOCKED_IPS = ['172.10.0.11', '172.10.0.12']

def ignore_ip_middleware(app):
    def middleware(request):
        if request.remote_addr in BLOCKED_IPS:
            return 'Request from this IP address is not allowed', 403
        return app(request)
    return middleware

