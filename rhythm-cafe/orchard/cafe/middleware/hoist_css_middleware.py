# css is inline based on each file
# so this takes all the css and puts it at the top
# no optimisation, that's a seperate step probably

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

            matches = []
            def substitute(match):
                matches.append(match)
                return ''
            
            response_content = style_regex.sub(substitute, response_content)

            # matches now contains all the regex matches, turn it into one big css string
            css_content = r"<style>" + "\n".join(match.groups()[0] for match in matches) + r"</style>"

            print(css_content)
            # which gets placed into the head. we've put a marker in head.jinja to do the replace on.
            response_content = response_content.replace("<!-- HOISTED_CSS -->", css_content, 1)

            response.content = response_content.encode(response.charset) 


        return response

    return middleware