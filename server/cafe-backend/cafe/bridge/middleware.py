# Vendored from django-bridge 0.4
from string import ascii_lowercase
from django.http.request import HttpRequest

import json
from pathlib import Path

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.templatetags.static import static

from .response import BaseResponse, RedirectResponse

BRIDGE_PARAM = "_bridge"

def string_only_az_and_dashes(s: str) -> bool:
    return all(c in ascii_lowercase or c == '-' for c in s)

class DjangoBridgeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        is_bridge_request = BRIDGE_PARAM in request.GET

        # Strip the _bridge param so view code never sees it
        if is_bridge_request:
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
            use_pr_client = ALLOW_CLIENT_DEV_COOKIE and "_pr_client" in request.COOKIES
            VITE_BUNDLE_DIR = settings.DJANGO_BRIDGE.get("VITE_BUNDLE_DIR")
            VITE_DEVSERVER_URL = settings.DJANGO_BRIDGE.get("VITE_DEVSERVER_URL")
            pr_value = request.COOKIES.get("_pr_client", "")
            valid_pr_client = (
                use_pr_client
                and bool(pr_value)
                and string_only_az_and_dashes(pr_value)
                and bool(getattr(settings, "PR_DOMAIN", None))
            )
            if valid_pr_client:
                # PR deployment, JS/CSS comes from PR domain
                base_url = f"https://{pr_value}.{settings.PR_DOMAIN}"
                js = [f"{base_url}/main.js"]
                css = [f"{base_url}/main.css"]
                vite_react_refresh_runtime = None
            elif (use_dev_client or VITE_DEVSERVER_URL):
                # Development - Fetch JS/CSS from Vite server
                devserver_url = VITE_DEVSERVER_URL or "http://localhost:5173/static"
                js = [
                    devserver_url + "/@vite/client",
                    devserver_url + "/src/main.tsx",
                ]
                css = []
                vite_react_refresh_runtime = devserver_url + "/@react-refresh"
            elif VITE_BUNDLE_DIR:
                # prod - asset manifest is bundled with us
                asset_manifest = json.loads(
                    (Path(VITE_BUNDLE_DIR) / ".vite/manifest.json").read_text()
                )

                js = [
                    static(asset_manifest["src/main.tsx"]["file"]),
                ]
                css = [static(css_file) for css_file in asset_manifest["src/main.tsx"].get("css", [])]
                vite_react_refresh_runtime = None
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
