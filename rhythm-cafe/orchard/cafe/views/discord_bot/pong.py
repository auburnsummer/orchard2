from django.http import JsonResponse

def pong():
    return JsonResponse({
        "type": 0
    })