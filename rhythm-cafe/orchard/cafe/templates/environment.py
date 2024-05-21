from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader("cafe"),
    autoescape=select_autoescape()
)