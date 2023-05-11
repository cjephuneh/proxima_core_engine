from django.db import models

class MetaDataBase(models.Model):
    metadata = models.JSONField(
         null=True, blank=True,
        help_text="Metadata"
    )
    # A timestamp representing when this object was created.
    created_at = models.TimeField(auto_now_add=True)
    date_time_created_at = models.DateField(auto_now_add=True, null=True)

    # A timestamp reprensenting when this object was last updated.
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

        # By default, any model that inherits from `TimestampedModel` should
        # be ordered in reverse-chronological order. We can override this on a
        # per-model basis as needed, but reverse-chronological is a good
        # default ordering for most models.
        ordering = ['-created_at', '-updated_at', '-metadata']

