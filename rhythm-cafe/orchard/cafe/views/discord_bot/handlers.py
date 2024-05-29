from textwrap import dedent
from django.http import JsonResponse

def version():
    return JsonResponse({
        "type": 4,
        "data": {
            "content": dedent(f"""
                ## Bot Version

                `0.0.1`
            """),
            "flags": 1 << 6
        },
    })


HANDLERS = {
    "version": version
}