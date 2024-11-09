from django_minify_html.middleware import MinifyHtmlMiddleware


class ProjectMinifyHtmlMiddleware(MinifyHtmlMiddleware):
    minify_args = MinifyHtmlMiddleware.minify_args | {
        # minify_js does not correctly handle getters: https://github.com/wilsonzlin/minify-js/issues/24
        "minify_js": False,
    }