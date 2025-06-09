import uuid
from datetime import date

from django.contrib.postgres.fields import ArrayField
from django.db import models

from ..core.models import AuditedModelWithCreatedAndUpdated

# List of ethnic groups from
# https://design-system.service.gov.uk/patterns/equality-information/
# This list is specific to England.
ETHNIC_GROUPS = {
    "White": [
        "English, Welsh, Scottish, Northern Irish or British",
        "Irish",
        "Gypsy or Irish Traveller",
        "Any other White background",
    ],
    "Mixed or multiple ethnic groups": [
        "White and Black Caribbean",
        "White and Black African",
        "White and Asian",
        "Any other mixed or multiple ethnic background",
    ],
    "Asian or Asian British": [
        "Indian",
        "Pakistani",
        "Bangladeshi",
        "Chinese",
        "Any other Asian background",
    ],
    "Black, African, Caribbean or Black British": [
        "African",
        "Caribbean",
        "Any other Black, African or Caribbean background",
    ],
    "Other ethnic group": ["Arab", "Any other ethnic group"],
}


class Participant(AuditedModelWithCreatedAndUpdated):
    PREFER_NOT_TO_SAY = "Prefer not to say"
    ETHNIC_GROUP_CHOICES = [
        (group, group) for groups in ETHNIC_GROUPS.values() for group in groups
    ] + [(PREFER_NOT_TO_SAY, PREFER_NOT_TO_SAY)]

    first_name = models.TextField()
    last_name = models.TextField()
    gender = models.TextField()
    nhs_number = models.TextField()
    phone = models.TextField()
    email = models.EmailField()
    date_of_birth = models.DateField()
    ethnic_group = models.CharField(blank=True, null=True, choices=ETHNIC_GROUP_CHOICES)
    risk_level = models.TextField()
    extra_needs = models.JSONField(null=False, default=list, blank=True)

    @property
    def full_name(self):
        return " ".join([name for name in [self.first_name, self.last_name] if name])

    def age(self):
        today = date.today()
        if (today.month, today.day) >= (
            self.date_of_birth.month,
            self.date_of_birth.day,
        ):
            return today.year - self.date_of_birth.year
        else:
            return today.year - self.date_of_birth.year - 1

    def ethnic_group_category(self):
        matches = [
            category
            for category, groups in ETHNIC_GROUPS.items()
            if self.ethnic_group in groups
        ]
        return matches[0] if matches else None


class ParticipantAddress(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    participant = models.OneToOneField(
        Participant, on_delete=models.CASCADE, related_name="address"
    )
    lines = ArrayField(models.CharField(), size=5, blank=True)
    postcode = models.CharField(blank=True, null=True)


class ScreeningEpisode(AuditedModelWithCreatedAndUpdated):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)

    def screening_history(self):
        """
        Return all previous screening episodes, excluding this one, prefetching
        their appointment details as well.
        """
        return (
            ScreeningEpisode.objects.prefetch_related(
                "appointment_set__clinic_slot__clinic__setting__provider"
            )
            .filter(participant__pk=self.participant.pk)
            .exclude(pk=self.pk)
            .order_by("-created_at")
        )

    def previous(self) -> "ScreeningEpisode | None":
        """
        Return the last known screening episode
        """
        try:
            return self.screening_history()[0]
        except IndexError:
            return None


class Appointment(AuditedModelWithCreatedAndUpdated):
    class Status:
        CONFIRMED = "CONFIRMED"
        CANCELLED = "CANCELLED"
        DID_NOT_ATTEND = "DID_NOT_ATTEND"
        CHECKED_IN = "CHECKED_IN"
        SCREENED = "SCREENED"
        PARTIALLY_SCREENED = "PARTIALLY_SCREENED"
        ATTENDED_NOT_SCREENED = "ATTENDED_NOT_SCREENED"

    STATUS_CHOICES = {
        Status.CONFIRMED: "Confirmed",
        Status.CANCELLED: "Cancelled",
        Status.DID_NOT_ATTEND: "Did not attend",
        Status.CHECKED_IN: "Checked in",
        Status.SCREENED: "Screened",
        Status.PARTIALLY_SCREENED: "Partially screened",
        Status.ATTENDED_NOT_SCREENED: "Attended not screened",
    }

    screening_episode = models.ForeignKey(ScreeningEpisode, on_delete=models.CASCADE)
    clinic_slot = models.ForeignKey(
        "clinics.ClinicSlot",
        on_delete=models.CASCADE,
    )
    status = models.CharField(
        choices=STATUS_CHOICES, max_length=50, default=Status.CONFIRMED
    )
    reinvite = models.BooleanField(default=False)
    stopped_reasons = models.JSONField(null=True, blank=True)
