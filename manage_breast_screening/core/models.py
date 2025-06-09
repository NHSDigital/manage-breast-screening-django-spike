import uuid

from django.db import models
from simple_history.models import HistoricalRecords


class AuditedModel(models.Model):
    """
    Model that includes an audit trail with django-simple-history
    """

    class Meta:
        abstract = True

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    history = HistoricalRecords(inherit=True)


class AuditedModelWithCreatedAndUpdated(AuditedModel):
    """
        Model that includes an audit trail with django-simple-history, and also created_at, updat
    ed_at fields
        which can be used for ordering records.
    """

    class Meta:
        abstract = True
        ordering = ["created_at"]
        get_latest_by = ["created_at"]

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
