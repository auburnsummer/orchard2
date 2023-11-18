from orchard.projects.v1.migrations.aaaaa_add_user_table import AddUserTable
from orchard.projects.v1.migrations.bbbbb_add_discord_credentials_table import AddDiscordCredentialsTable
from orchard.projects.v1.migrations.ccccc_add_publisher_table import AddPublisherTable
from orchard.projects.v1.migrations.ddddd_add_rd_level_table import AddRDLevelTable


ALL_MIGRATIONS = [
    AddUserTable(),
    AddDiscordCredentialsTable(),
    AddPublisherTable(),
    AddRDLevelTable()
]