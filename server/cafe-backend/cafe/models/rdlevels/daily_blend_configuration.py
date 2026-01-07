from django.db import models
from django.core.exceptions import ValidationError
from rules.contrib.models import RulesModel


class DailyBlendConfiguration(RulesModel):
    """
    Singleton configuration model for Daily Blend.
    Only one configuration row can exist.
    """
    webhook_urls = models.TextField(blank=True, default="")
    jsonata_script = models.TextField(blank=True, default="")

    def save(self, *args, **kwargs):
        """Ensure only one instance exists."""
        if not self.pk and DailyBlendConfiguration.objects.exists():
            raise ValidationError("Only one DailyBlendConfiguration instance is allowed.")
        return super().save(*args, **kwargs)

    @classmethod
    def get_config(cls):
        """Get or create the singleton configuration instance."""
        config, _ = cls.objects.get_or_create(pk=1)
        return config
    
    def to_dict(self):
        """Return configuration as a dictionary."""
        return {
            "webhook_urls": self.webhook_urls,
            "jsonata_script": self.jsonata_script,
        }