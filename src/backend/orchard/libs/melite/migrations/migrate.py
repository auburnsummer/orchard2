from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
import apsw.bestpractice

from apsw import Connection
from loguru import logger

apsw.bestpractice.apply(apsw.bestpractice.recommended)

ORIGIN = "origin"  # the first version is always called "origin".
MELITE_TABLE = "__melite"

def create_melite_table(conn: Connection):
    "Create the internal table used for tracking the schema version."
    # pypika's DSL can't do the CHECK or STRICT here.
    conn.execute(f"""
    CREATE TABLE "{MELITE_TABLE}" (
        "id" INT PRIMARY KEY CHECK (id = 0),
        "melite_version" TEXT NOT NULL
    ) STRICT;
""")
    conn.execute(f"""
    INSERT INTO "{MELITE_TABLE}" VALUES (0, 'origin')
    """)


def get_current_version(conn: Connection) -> str:
    "Read the current schema version from the database. Creates the table if it doesn't exist."
    q = f"""--sql
    SELECT "melite_version" FROM "{MELITE_TABLE}"
    WHERE "{MELITE_TABLE}"."id" = 0
    """
    try:
        cursor = conn.execute(q)
    except apsw.SQLError:
        logger.warning("__melite table does not exist. Making it now...")
        create_melite_table(conn)
        cursor = conn.execute(q)
    row = next(cursor)
    return row[0]



class Migrator(ABC):
    """
    Abstract base class for any individual schema upgrade.
    """

    @property
    @abstractmethod
    def migrate_from(self) -> str:
        "The version this migrator starts from."

    @property
    @abstractmethod
    def migrate_to(self) -> str:
        "The version this migrator upgrades the schema to."

    @abstractmethod
    def upgrade(self, conn: Connection):
        "Run the migration."

class NoMigrationException(Exception):
    pass

def migrate(conn: Connection, target_version: str | None, migrators: List[Migrator]):
    """
    Run a migration from the target version to the current version. If None is given
    as the target version, run the migration to the latest.
    """
    current_version = get_current_version(conn)
    if current_version == target_version:
        return

    logger.info(f"Beginning migration to {target_version or 'latest'}")

    while True:
        current_version = get_current_version(conn)
        if current_version == target_version:
            break
        for migrator in migrators:
            if migrator.migrate_from == current_version:
                next_version = migrator.migrate_to
                logger.info(f"version {current_version} -> {next_version}")
                migrator.upgrade(conn)
                conn.execute(f"""--sql
                UPDATE {MELITE_TABLE}
                    SET "melite_version" = ?
                    WHERE "id" = 0
                """, [next_version])
                break
        else:
            if target_version is None:
                break
            raise NoMigrationException(f"No migration found for version {current_version}.")