import json
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.exceptions import InvalidSignature

from orchard.settings import DISCORD_PUBLIC_KEY

from .handlers import HANDLERS

verify_key = Ed25519PublicKey.from_public_bytes(bytes.fromhex(DISCORD_PUBLIC_KEY))

class HttpResponseUnauthorized(HttpResponse):
    status_code = 401

@csrf_exempt
def entry(request):
    # check the discord headers.
    headers = request.headers
    try:
        sig = headers["X-Signature-Ed25519"]
        timestamp = headers["X-Signature-Timestamp"]
    except KeyError:
        return HttpResponseUnauthorized('Discord headers missing.')
    
    payload = request.body
    to_verify = timestamp.encode("ascii") + payload

    try:
        verify_key.verify(bytes.fromhex(sig), to_verify)
    except InvalidSignature:
        return HttpResponseUnauthorized('Signature is incorrect.')
    
    data = json.loads(payload)

    # handle ping.
    if data['type'] == 1:
        return JsonResponse({
            "type": 1
        })
    
    # commands.
    if data['type'] == 2:
        command_name = data['data']['name']
        if command_name in HANDLERS:
            return HANDLERS[command_name](data)
        
    return HttpResponseNotFound('Not sure how to handle this type.')