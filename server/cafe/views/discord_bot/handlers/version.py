from django.http import HttpResponseRedirect, JsonResponse
from textwrap import dedent

from .utils import ephemeral_response

def version(_data):
    content = dedent(f"""
        ## Bot Version

        `0.0.1`    
    """)
    return ephemeral_response(content)