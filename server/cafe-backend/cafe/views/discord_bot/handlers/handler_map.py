from .version import version
from .connectgroup import connectgroup
from .viewgroup import viewgroup
from .add import add, add_delegated
from .become_admin import becomeadmin

HANDLERS = {
    "version": version,
    "connectgroup": connectgroup,
    "viewgroup": viewgroup,
    "Add to Rhythm Café": add,
    "Add to Rhythm Café (delegated)": add_delegated,
    "becomeadmin": becomeadmin
}