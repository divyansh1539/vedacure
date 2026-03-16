from django.shortcuts import redirect
from django.urls import reverse

class AuthenticationMiddleware:
    """
    Middleware to protect all pages and redirect unauthenticated users to login.
    Allows access to login, signup, admin, and password reset pages without authentication.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # URLs that don't require authentication
        self.public_urls = [
            '/login/',
            '/signup/',
            '/admin/',
            '/password-reset/',
            '/password-reset/done/',
            '/reset/',
            '/reset/done/',
        ]
    
    def __call__(self, request):
        # Check if URL is public
        is_public = any(request.path.startswith(url) for url in self.public_urls)
        
        # Check if user is authenticated
        is_authenticated = request.user.is_authenticated
        
        # If not public and not authenticated, redirect to login
        if not is_public and not is_authenticated:
            return redirect('login')
        
        response = self.get_response(request)
        return response