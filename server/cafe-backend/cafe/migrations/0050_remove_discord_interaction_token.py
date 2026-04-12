from django.db import migrations


class Migration(migrations.Migration):
    """
    The migration that originally added discord_interaction_token to
    RDLevelPrefillResult was deleted, but the column still exists in the
    database. This migration drops the stale column using
    SeparateDatabaseAndState so the state-side is a no-op (the model no
    longer has the field) while the database-side removes the column.
    """

    dependencies = [
        ('cafe', '0049_addsession_prefill'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    sql='ALTER TABLE "cafe_rdlevelprefillresult" DROP COLUMN "discord_interaction_token"',
                    reverse_sql=migrations.RunSQL.noop,
                ),
            ],
            state_operations=[],
        ),
    ]
