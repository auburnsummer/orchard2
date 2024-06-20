# strip the <style data-hoist=true> tags in templates
# these are parsed and added as part of the meta/all_styles.css route instead

import re

def hoist_css_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        response = get_response(request)
        
        # we can't alter streaming responses in the way we want, so just let it go.
        if response.streaming:
            return response
        
        # we're only interested in HTML responses.
        if 'content-type' in response.headers and response.headers['content-type'].startswith('text/html'):
            response_content = response.content.decode(response.charset)
            # all css that should be hoisted contains data-hoist=true attribute.
            style_regex = re.compile(r"<style data-hoist=\"true\">([\w\W]+?)<\/style>")

            def substitute(match):
                return ''
            
            response_content = style_regex.sub(substitute, response_content)

            response.content = response_content.encode(response.charset) 


        return response

    return middleware