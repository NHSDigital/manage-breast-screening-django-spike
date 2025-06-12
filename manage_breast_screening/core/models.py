import uuid

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class BaseModel(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AuditLog(models.Model):
    class Operations:
        CREATE = "create"
        UPDATE = "update"
        DELETE = "delete"

    OperationChoices = [
        (Operations.CREATE, "Create"),
        (Operations.UPDATE, "Update"),
        (Operations.DELETE, "Delete"),
    ]

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT, null=True)
    object_id = models.UUIDField()
    content_object = GenericForeignKey("content_type", "object_id")
    operation = models.CharField(choices=OperationChoices)
    changes = models.JSONField()
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True
    )
    system_update_id = models.CharField(null=True)

    def __str__(self):
        return f"{self.get_operation_display()} {self.content_type} ({self.object_id})"

    @classmethod
    def log_actions(cls, objects, operation, actor):
        log_entry_list = [
            cls(
                content_object=object,
                operation=operation,
                changes={},
                actor=actor,
            )
            for object in objects
        ]
        if len(log_entry_list) == 1:
            log_entry_list[0].save()
        else:
            cls.objects.bulk_create(log_entry_list)
