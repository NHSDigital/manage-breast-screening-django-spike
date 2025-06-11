from django.urls import reverse

from ..core.utils.date_formatting import format_date, format_relative_date, format_time
from ..participants.models import Appointment
from ..participants.presenters import ParticipantPresenter

Status = Appointment.Status


def status_colour(status):
    """
    Color to render the status tag
    """
    match status:
        case Status.CHECKED_IN:
            return ""  # no colour will get solid dark blue
        case Status.SCREENED:
            return "green"
        case Status.DID_NOT_ATTEND | Status.CANCELLED:
            return "red"
        case Status.ATTENDED_NOT_SCREENED | Status.PARTIALLY_SCREENED:
            return "orange"
        case _:
            return "blue"  # default blue


def present_secondary_nav(id):
    """
    Build a secondary nav for reviewing the information of screened/partially screened appointments.
    """
    return [
        {
            "id": "all",
            "text": "Appointment details",
            "href": reverse("mammograms:start_screening", kwargs={"id": id}),
            "current": True,
        },
        {"id": "medical_information", "text": "Medical information", "href": "#"},
        {"id": "images", "text": "Images", "href": "#"},
    ]


class AppointmentPresenter:
    def __init__(self, appointment):
        self._appointment = appointment
        self._last_known_screening = appointment.screening_episode.previous()

        self.allStatuses = Status
        self.id = appointment.id
        self.clinic_slot = ClinicSlotPresenter(appointment.clinic_slot)
        self.participant = ParticipantPresenter(
            appointment.screening_episode.participant
        )

    @property
    def participant_url(self):
        return self.participant.url

    @property
    def status(self):
        colour = status_colour(self._appointment.status)

        return {
            "classes": f"nhsuk-tag--{colour} app-nowrap" if colour else "app-nowrap",
            "text": self._appointment.get_status_display(),
            "key": self._appointment.status,
            "is_confirmed": self._appointment.status == Status.CONFIRMED,
        }

    @property
    def last_known_screening(self):
        return (
            {
                "date": format_date(self._last_known_screening.created_at),
                "relative_date": format_relative_date(
                    self._last_known_screening.created_at
                ),
                # TODO: the current model doesn't allow for knowing the type and location of a historical screening
                # if it is not tied to one of our clinic slots.
                "location": None,
                "type": None,
            }
            if self._last_known_screening
            else {}
        )


class ClinicSlotPresenter:
    def __init__(self, clinic_slot):
        self._clinic_slot = clinic_slot
        self._clinic = clinic_slot.clinic

        self.clinic_id = self._clinic.id

    @property
    def clinic_type(self):
        return self._clinic.get_type_display().capitalize()

    @property
    def slot_time_and_clinic_date(self):
        clinic_slot = self._clinic_slot
        clinic = self._clinic

        return f"{format_time(clinic_slot.starts_at)} ({clinic_slot.duration_in_minutes} minutes) - {format_date(clinic.starts_at)} ({format_relative_date(clinic.starts_at)})"
