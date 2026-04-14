from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("cafe", "0052_add_session_phase_choices"),
    ]

    operations = [
        migrations.RunSQL(
            sql='DROP TABLE IF EXISTS "cafe_discordaddlevelsession"',
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
