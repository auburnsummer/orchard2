
from orchard.projects.v1.routes.interactions.spec import ApplicationCommand, ApplicationCommandType

version = ApplicationCommand(
    name="version",
    description="Print the version of the bot.",
)

def version_command():
    pass

register = ApplicationCommand(
    name="register",
    description="Register this discord server with Rhythm Cafe."
)

console = ApplicationCommand(
    name="console",
    description="Open the Publisher Administration Console."
)

# Message types cannot have a description.
add = ApplicationCommand(
    name="add",
    type=ApplicationCommandType.MESSAGE
)

ALL_COMMANDS = [
    version,
    register,
    console,
    add
]