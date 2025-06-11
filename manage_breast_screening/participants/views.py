from logging import getLogger

from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Participant
from .presenters import ParticipantPresenter

logger = getLogger(__name__)


def show(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    presenter = ParticipantPresenter(participant)

    return render(
        request,
        "show.jinja",
        context={
            "participant": presenter,
            "heading": participant.full_name,
            "back_link": {
                "text": "Back to participants",
                "href": reverse("participants:index"),
            },
        },
    )
