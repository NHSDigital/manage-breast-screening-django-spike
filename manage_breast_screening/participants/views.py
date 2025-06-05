from logging import getLogger

from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Appointment, Participant
from .presenters import ParticipantPresenter

logger = getLogger(__name__)


def get_back_link(request):
    appointment_id = request.GET.get("appointment_id")
    if appointment_id and not Appointment.objects.filter(pk=appointment_id).exists():
        logger.error(f"Invalid appointment id: {appointment_id}")
        raise Http404

    return (
        {
            "text": "Back to appointment",
            "href": reverse(
                "mammograms:start_screening", kwargs={"id": appointment_id}
            ),
        }
        if appointment_id
        else {
            "text": "Back to participants",
            "href": reverse("participants:index"),
        }
    )


def show(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    presenter = ParticipantPresenter(participant)
    back_link = get_back_link(request)

    return render(
        request,
        "show.jinja",
        context={
            "participant": presenter,
            "heading": participant.full_name,
            "back_link": back_link,
        },
    )
