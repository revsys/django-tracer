import uuid


class RequestID(object):
    """
    Adds a UUID per request to all requests for traceability
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.id = str(uuid.uuid4())

        response = self.get_response(request)

        # Add Request-ID header to all responses
        response['X-Request-ID'] = request.id

        return response
