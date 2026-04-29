# Vendored from django-bridge 0.4

import json
from pathlib import Path

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.templatetags.static import static

from .response import BaseResponse, RedirectResponse

BRIDGE_PARAM = "_bridge"


class DjangoBridgeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        is_bridge_request = BRIDGE_PARAM in request.GET

        # Strip the _bridge param so view code never sees it
        if is_bridge_request:
            request.GET = request.GET.copy()
            del request.GET[BRIDGE_PARAM]

        response = self.get_response(request)

        if isinstance(response, StreamingHttpResponse):
            return response

        if response.status_code == 301:
            return response

        # If the request was made via the bridge client
        if is_bridge_request:
            # Convert redirect responses to a JSON response with a `redirect` status
            # This allows the client code to handle the redirect
            if response.status_code == 302:
                return RedirectResponse(response["Location"])

            return response

        # Regular browser request
        # If the response is a Django Bridge response, wrap it in our bootstrap template
        # to load the React SPA and render the response data.
        if isinstance(response, BaseResponse):
            ALLOW_CLIENT_DEV_COOKIE = settings.DJANGO_BRIDGE.get("ALLOW_CLIENT_DEV_COOKIE", False)
            use_dev_client = ALLOW_CLIENT_DEV_COOKIE and "_dev_client" in request.COOKIES

            VITE_BUNDLE_DIR = settings.DJANGO_BRIDGE.get("VITE_BUNDLE_DIR")
            VITE_DEVSERVER_URL = settings.DJANGO_BRIDGE.get("VITE_DEVSERVER_URL")
            if VITE_BUNDLE_DIR and not use_dev_client:
                # Production - Use asset manifest to find URLs to bundled JS/CSS
                asset_manifest = json.loads(
                    (Path(VITE_BUNDLE_DIR) / ".vite/manifest.json").read_text()
                )

                js = [
                    static(asset_manifest["src/main.tsx"]["file"]),
                ]
                css = asset_manifest["src/main.tsx"].get("css", [])
                vite_react_refresh_runtime = None

            elif VITE_DEVSERVER_URL or use_dev_client:
                # Development - Fetch JS/CSS from Vite server
                devserver_url = VITE_DEVSERVER_URL or "http://localhost:5173/static"
                js = [
                    devserver_url + "/@vite/client",
                    devserver_url + "/src/main.tsx",
                ]
                css = []
                vite_react_refresh_runtime = devserver_url + "/@react-refresh"

            else:
                raise ImproperlyConfigured(
                    "DJANGO_BRIDGE['VITE_BUNDLE_DIR'] (production) or DJANGO_BRIDGE['VITE_DEVSERVER_URL'] (development) must be set"
                )

            # Wrap the response with our bootstrap template
            initial_response = json.loads(response.content.decode("utf-8"))
            new_response = render(
                request,
                "django_bridge/bootstrap.html",
                {
                    "metadata": initial_response.get("metadata"),
                    "initial_response": json.loads(response.content.decode("utf-8")),
                    "js": js,
                    "css": css,
                    "vite_react_refresh_runtime": vite_react_refresh_runtime,
                    "dev_cookie_active": use_dev_client,
                },
            )

            # Copy status_code and cookies from the original response
            new_response.status_code = response.status_code
            new_response.cookies = response.cookies

            return new_response

        return response
