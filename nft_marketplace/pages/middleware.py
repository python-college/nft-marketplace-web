class SessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.session_id = request.COOKIES.get('session_id')
        request.address_wallet = request.COOKIES.get('address_wallet')
        response = self.get_response(request)
        return response
