from ..core.utils.date_formatting import format_date, format_time_range
from ..core.utils.string_formatting import sentence_case
from .models import Clinic


class ClinicsPresenter:
    def __init__(self, filtered_clinics, filter, counts_by_filter):
        self.clinics = [ClinicPresenter(clinic) for clinic in filtered_clinics]
        self.counts_by_filter = counts_by_filter
        self.filter = filter

    @property
    def heading(self):
        if self.filter == "today":
            return "Today’s clinics"
        elif self.filter == "upcoming":
            return "Upcoming clinics"
        elif self.filter == "completed":
            return "Completed clinics this week"
        else:
            return "All clinics this week"


class ClinicPresenter:
    STATUS_COLORS = {
        Clinic.State.SCHEDULED: "blue",  # default blue
        Clinic.State.IN_PROGRESS: "blue",
        Clinic.State.CLOSED: "grey",
    }

    def __init__(self, clinic):
        self._clinic = clinic
        self.id = clinic.id
        self.starts_at = format_date(clinic.starts_at)
        self.session_type = clinic.session_type().capitalize()
        self.number_of_slots = clinic.clinic_slots.count()
        self.location_name = sentence_case(clinic.setting.name)
        self.time_range = format_time_range(clinic.time_range())
        self.type = clinic.get_type_display()
        self.risk_type = clinic.get_risk_type_display()

    @property
    def state(self):
        return {
            "text": self._clinic.get_state_display(),
            "classes": "nhsuk-tag--" + self.STATUS_COLORS[self._clinic.state],
        }

    @property
    def setting_name(self):
        return self._clinic.setting.name

