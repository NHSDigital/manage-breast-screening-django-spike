import logging

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.generic import FormView

from manage_breast_screening.clinics.models import Appointment

from ..clinics.models import Appointment
from .forms import (
    AppointmentCannotGoAheadForm,
    AskForMedicalInformationForm,
    RecordMedicalInformationForm,
    ScreeningAppointmentForm,
)

Status = Appointment.Status

logger = logging.getLogger(__name__)


def status_color(status):
    """
    Color to render the status tag
    """
    match status:
        case Status.CHECKED_IN:
            return ""  # no colour will get solid dark blue
        case Status.SCREENED:
            return "green"
        case (Status.DID_NOT_ATTEND, Status.CANCELLED):
            return "red"
        case (Status.ATTENDED_NOT_SCREENED, Status.PARTIALLY_SCREENED):
            return "orange"
        case _:
            return "blue"  # default blue


class StartScreening(FormView):
    template_name = "record_a_mammogram/start_screening.jinja"
    form_class = ScreeningAppointmentForm

    def get_appointment(self):
        id = self.kwargs["id"]

        return Appointment.objects.prefetch_related(
            "clinic_slot", "screening_episode__participant"
        ).get(pk=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        appointment = self.get_appointment()

        context["appointment"] = appointment
        context["clinic_slot"] = appointment.clinic_slot
        context["participant"] = appointment.screening_episode.participant

        context["status"] = {
            "colour": status_color(appointment.status),
            "text": appointment.get_status_display(),
            "key": appointment.status,
        }
        context["Status"] = Status

        if appointment.status in [
            appointment.Status.SCREENED,
            appointment.Status.PARTIALLY_SCREENED,
        ]:
            context["secondary_nav_items"] = build_secondary_nav(appointment.pk)

        last_known_screening = appointment.screening_episode.previous()

        # TODO: the current model doesn't allow for knowing the type and location of a historical screening
        # if it is not tied to one of our clinic slots, so we can't easily populate historical
        # screening episodes at the moment.
        context["last_known_screening"] = (
            {"date": last_known_screening.created_at, "location": None, "type": None}
            if last_known_screening
            else {}
        )

        return context

    def form_valid(self, form):
        form.save()

        if form.cleaned_data["decision"] == "continue":
            return redirect("record_a_mammogram:ask_for_medical_information")
        else:
            return redirect("record_a_mammogram:appointment_cannot_go_ahead")


class AskForMedicalInformation(FormView):
    template_name = "record_a_mammogram/ask_for_medical_information.jinja"
    form_class = AskForMedicalInformationForm

    def form_valid(self, form):
        form.save()

        if form.cleaned_data["decision"] == "continue":
            return redirect("record_a_mammogram:record_medical_information")
        else:
            return redirect("record_a_mammogram:awaiting_images")


class RecordMedicalInformation(FormView):
    template_name = "record_a_mammogram/record_medical_information.jinja"
    form_class = RecordMedicalInformationForm

    def form_valid(self, form):
        form.save()

        if form.cleaned_data["decision"] == "continue":
            return redirect("record_a_mammogram:awaiting_images")
        else:
            return redirect("record_a_mammogram:appointment_cannot_go_ahead")


class AppointmentCannotGoAhead(FormView):
    template_name = "record_a_mammogram/appointment_cannot_go_ahead.jinja"
    form_class = AppointmentCannotGoAheadForm


def awaiting_images(request):
    return render(request, "record_a_mammogram/awaiting_images.jinja", {})


@require_http_methods(["POST"])
def check_in(request, id):
    appointment = get_object_or_404(Appointment, pk=id)
    appointment.status = Appointment.Status.CHECKED_IN
    appointment.save()

    return redirect("record_a_mammogram:start_screening", id=id)


def build_secondary_nav(id):
    """
    Build a secondary nav for reviewing the information of screened/partially screened appointments.
    """
    return [
        {
            "id": "all",
            "text": "Appointment details",
            "href": reverse("record_a_mammogram:start_screening", kwargs={"id": id}),
            "current": True,
        },
        {"id": "medical_information", "text": "Medical information", "href": "#"},
        {"id": "images", "text": "Images", "href": "#"},
    ]
