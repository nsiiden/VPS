class AuditMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        if request.user.is_authenticated:
            from .models import AuditTrail  # Defer import to avoid circular import issues
            ip_address = request.META.get('REMOTE_ADDR')
            user_agent = request.META.get('HTTP_USER_AGENT')
            action = f"{request.method} {request.get_full_path()}"
            AuditTrail.objects.create(user=request.user, action=action, ip_address=ip_address, user_agent=user_agent)
        
        return response
