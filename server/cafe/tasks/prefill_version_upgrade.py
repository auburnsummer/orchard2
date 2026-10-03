from huey.contrib.djhuey import db_periodic_task
from huey import crontab
from loguru import logger

from cafe.models.rdlevels.prefill import RDLevelPrefillResult

BATCH_SIZE = 10

from vitals.vitals import PREFILL_VERSION

CURRENT_PREFILL_VERSION = PREFILL_VERSION

PROPS_ADDED_ON_EACH_PREFILL_VERSION_UPGRADE = {
    2: [
        "has_classics",
        "has_oneshots",
        "has_squareshots",
        "has_freezeshots",
        "has_burnshots",
        "has_holdshots",
        "has_triangleshots",
        "has_skipshots",
        "has_subdivs",
        "has_synco",
        "has_freetimes",
        "has_holds",
        "has_window_dance",
        "has_rdcode",
        "has_cpu_rows",
        "total_hits_approx",
    ]
}

@db_periodic_task(crontab(minute='*', strict=True), priority=0, expires=2)
def prefill_version_upgrade():
    # levels that need upgrading will have prefill_version less than CURRENT_PREFILL_VERSION
    from cafe.models.rdlevels.rdlevel import RDLevel
    from cafe.tasks.run_prefill import run_prefill
    levels_to_upgrade = RDLevel.objects.filter(prefill_version__lt=CURRENT_PREFILL_VERSION)[:BATCH_SIZE]
    if len(levels_to_upgrade) == 0:
        return
    logger.info(f"Upgrading {len(levels_to_upgrade)} levels to prefill version {CURRENT_PREFILL_VERSION}")
    for level in levels_to_upgrade:
        logger.info(f"Upgrading level {level.id} from prefill version {level.prefill_version} to {CURRENT_PREFILL_VERSION}")
        rdlevel_prefill_result = RDLevelPrefillResult.objects.create(
            url=level.rdzip_url,
            version=CURRENT_PREFILL_VERSION,
            user=level.submitter,
            prefill_type="new",
            club=level.club
        )
        run_prefill.call_local(rdlevel_prefill_result.id)
        rdlevel_prefill_result.refresh_from_db()
        if not rdlevel_prefill_result.ready:
            continue # todo: we should send a sentry event here I think
        # which props are we replacing?
        props_to_update = []
        for v in range(level.prefill_version + 1, CURRENT_PREFILL_VERSION + 1):
            props_to_update.extend(PROPS_ADDED_ON_EACH_PREFILL_VERSION_UPGRADE.get(v, []))
        for prop in props_to_update:
            setattr(level, prop, rdlevel_prefill_result.data.get(prop))
        level.prefill_version = CURRENT_PREFILL_VERSION
        level.save()

