from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods

from .presenters import ClinicsPresenter, ClinicPresenter
from .presenters import AppointmentListPresenter

from .models import Clinic
from ..participants.models import Appointment

STATUS_COLORS = {
    Clinic.State.SCHEDULED: "blue",  # default blue
    Clinic.State.IN_PROGRESS: "blue",
    Clinic.State.CLOSED: "grey",
}


def clinic_list(request, filter="today"):
    clinics = Clinic.objects.prefetch_related("setting").by_filter(filter)
    counts_by_filter = Clinic.filter_counts()
    presenter = ClinicsPresenter(clinics, filter, counts_by_filter)
    return render(
        request,
        "index.jinja",
        context={"presenter": presenter},
    )


def clinic(request, id, filter="remaining"):
    clinic = Clinic.objects.prefetch_related("setting").get(id=id)
    presented_clinic = ClinicPresenter(clinic)
    appointments = Appointment.clinic_appointments_by_filter(
        clinic, filter
    ).select_related("clinic_slot", "screening_episode__participant")
    counts_by_filter = Appointment.counts_by_filter(clinic)
    presented_appointment_list = AppointmentListPresenter(
        appointments, filter, counts_by_filter
    )
    return render(
        request,
        "show.jinja",
        context={
            "presented_clinic": presented_clinic,
            "presented_appointment_list": presented_appointment_list,
        },
    )


@require_http_methods(["POST"])
def check_in(_request, id, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    appointment.status = Appointment.Status.CHECKED_IN
    appointment.save()

    return redirect("clinics:show", id=id)
