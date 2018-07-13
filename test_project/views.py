
from django.http import HttpResponse


def request_test_view(request):
    return HttpResponse("VIEW")
