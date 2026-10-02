from .version import version
from .connectgroup import connectgroup
from .viewgroup import viewgroup
from .add import add, add_delegated, add_step
from .become_admin import becomeadmin

HANDLERS = {
    "version": version,
    "connectgroup": connectgroup,
    "viewgroup": viewgroup,
    "Add to Rhythm Café": add,
    "Add to Rhythm Café (delegated)": add_delegated,
    "becomeadmin": becomeadmin
}

MESSAGE_COMPONENT_HANDLERS = {
    "Add to Rhythm Café": add_step,
    "Add to Rhythm Café (delegated)": add_step,
}