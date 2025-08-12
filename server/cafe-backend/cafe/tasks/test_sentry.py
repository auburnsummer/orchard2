"""
Test task for verifying Sentry integration with Huey tasks.
This task can be removed after testing.
"""
from huey.contrib.djhuey import task
import sentry_sdk


@task()
def test_sentry_integration():
    """
    Test task that intentionally raises an exception to verify Sentry integration.
    
    Usage from Django shell:
        from cafe.tasks.test_sentry import test_sentry_integration
        test_sentry_integration()
    """
    try:
        # Intentionally raise an exception
        raise ValueError("Test exception for Sentry integration")
    except Exception as e:
        with sentry_sdk.push_scope() as scope:
            scope.set_context("test_task", {
                "task": "test_sentry_integration",
                "purpose": "Testing Sentry error reporting"
            })
            sentry_sdk.capture_exception(e)
        # Re-raise to test both captured and uncaught scenarios
        raise
