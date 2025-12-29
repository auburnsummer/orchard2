import django
from django.apps import AppConfig
import django_bridge.response

class CafeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cafe'

    def ready(self):
        """
        OK so what nonsense are we doing here?
        basically django-bridge Response class normally uses the telepath library (which
        is aliased to JSContext) to serialize data to send to the frontend. However, we
        don't want to include telepath in our client bundle, so we are monkeypatching the
        JSContext class with a dummy class that just passes data through as-is.

        Telepath does things like converting Django forms, etc to JS objects, but we don't
        use those features, we're always only sending plain dicts/lists/strings/numbers/bools.
        
        It also does some "clever" serialization of long strings where
        it tries to take repeated strings and store them only once and otherwise store a 
        { _ref: } object. This is kinda annoying because we'd have to reimplement the
        client logic, and in addition, anyone who consumes our frankenstein API would also
        need to implement that logic.
        
        So instead, we just bypass telepath entirely.
        
        Reference:
        https://github.com/kaedroho/django-bridge/blob/ab138e392e54481faa556837e2ea429535de022b/python/django_bridge/response.py#L37

        Yes, this is a big hack. My eventual plan is to stop using django-bridge altogether
        and do some sort of SSR thing instead, but for now this will do.
        """
        class ReplacementJSContext():
            def pack(self, args):
                return args
        
        django_bridge.response.JSContext = ReplacementJSContext