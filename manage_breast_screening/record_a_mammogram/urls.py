from django.urls import path
from django.views.generic import RedirectView

from . import forms, views

app_name = "clinics"

urlpatterns = [
    path(
        "",
        RedirectView.as_view(pattern_name="record:step"),
        name="index",
        kwargs={"step_id": forms.WIZARD.start_step.id, "wizard": forms.WIZARD},
    ),
    path(
        "<str:step_id>/",
        views.wizard_step,
        name="step",
        kwargs={"wizard": forms.WIZARD},
    ),
]
