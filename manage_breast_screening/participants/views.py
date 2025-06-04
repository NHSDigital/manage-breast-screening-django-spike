from django.shortcuts import get_object_or_404, render

from .models import Participant
from .presenters import ParticipantPresenter


def show(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    presenter = ParticipantPresenter(participant)

    return render(
        request,
        "show.jinja",
        context={"participant": presenter, "heading": participant.full_name},
    )
