from orchard.projects.v1.migrations.aaaaa_add_user_table import AddUserTable
from orchard.projects.v1.migrations.bbbbb_add_discord_credentials_table import AddDiscordCredentialsTable
from orchard.projects.v1.migrations.ccccc_add_publisher_table import AddPublisherTable


ALL_MIGRATIONS = [
    AddUserTable(),
    AddDiscordCredentialsTable(),
    AddPublisherTable()
]