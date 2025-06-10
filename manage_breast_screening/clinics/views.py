from django.shortcuts import render

from manage_breast_screening.clinics.presenters import ClinicsPresenter, ClinicPresenter

from .models import Clinic

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


def clinic(request, id):
    clinic = Clinic.objects.prefetch_related("setting").get(id=id)
    presented_clinic = ClinicPresenter(clinic)
    return render(
        request,
        "show.jinja",
        context={"presented_clinic": presented_clinic},
    )
