from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
import apsw.bestpractice

from apsw import Connection
from loguru import logger
from orchard.libs.melite.base import MeliteStruct
from orchard.libs.melite.insert import insert
from orchard.libs.melite.select import Select
from orchard.libs.melite.update import update

apsw.bestpractice.apply(apsw.bestpractice.recommended)

ORIGIN = "origin"  # the first version is always called "origin".
MELITE_TABLE = "__melite"

class MeliteMetadata(MeliteStruct):
    table_name = MELITE_TABLE
    id: int
    melite_version: str

class MeliteMigrationException(Exception):
    pass

def create_melite_table(conn: Connection):
    "Create the internal table used for tracking the schema version."
    conn.execute(f"""
    CREATE TABLE "{MELITE_TABLE}" (
        "id" INT PRIMARY KEY CHECK (id = 0),
        "melite_version" TEXT NOT NULL
    ) STRICT;
""")
    insert(conn, MeliteMetadata(
        id=0,
        melite_version='origin'
    ))

def get_current_version(conn: Connection) -> MeliteMetadata:
    try:
        metadata = Select(conn, MeliteMetadata).by_id(0)
        if metadata:
            return metadata
        else:
            raise MeliteMigrationException("Melite table exists but no value.")
    except apsw.SQLError:
        create_melite_table(conn)
        return get_current_version(conn)




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


def migrate(conn: Connection, target_version: str | None, migrators: List[Migrator]):
    """
    Run a migration from the target version to the current version. If None is given
    as the target version, run the migration to the latest.
    """
    current_version = get_current_version(conn)
    if current_version.melite_version == target_version:
        return

    logger.info(f"Beginning migration to {target_version or 'latest'}")

    while True:
        current_version = get_current_version(conn)
        if current_version.melite_version == target_version:
            break
        for migrator in migrators:
            if migrator.migrate_from == current_version.melite_version:
                next_version = migrator.migrate_to
                logger.info(f"version {current_version.melite_version} -> {next_version}")
                migrator.upgrade(conn)
                current_version.melite_version = next_version
                update(conn, current_version)
                break
        else:
            if target_version is None:
                break
            raise MeliteMigrationException(f"No migration found for version {current_version.melite_version}.")