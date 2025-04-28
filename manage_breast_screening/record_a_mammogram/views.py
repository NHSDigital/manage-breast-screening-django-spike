import logging

from django.forms import ModelForm
from django.shortcuts import redirect, render

from manage_breast_screening.form_utils import ChoiceStep

from .forms import Wizard

logger = logging.getLogger(__name__)


def wizard_step(request, step_id: str, wizard: Wizard):
    """
    Generic view to handle a step in a wizard.

    This does basic form handling and redirects to the appropriate
    next step based on the user's selection.

    However, we do not do any checking that the step being visited is the
    expected one in the flow - the user is technically free to visit the steps
    in any order.
    """
    view_name = request.resolver_match.view_name

    try:
        step = wizard.get_step_by_id(step_id)
    except KeyError:
        # If a step no longer exists for some reason, go back to the start
        logging.error(
            f"Step {step_id} does not exist, redirecting to {wizard.start_step.id}"
        )
        return redirect(
            view_name,
            step_id=wizard.start_step.id,
        )

    template = step.template
    start_step = wizard.start_step

    if step == start_step and request.method == "GET":
        # TODO: initialise any wizard state
        pass

    match step:
        case ChoiceStep():
            return _handle_wizard_form(request, step, view_name)
        case _:
            return render(request, template, {"step": step})


def _handle_wizard_form(request, step, view_name):
    if request.method == "POST":
        form = step.form_class(request.POST)

        if form.is_valid():
            if isinstance(form, ModelForm):
                form.save()

            # TODO: at this point we might also want to
            # a) save progress to the session
            # b) update a back button stack

            # Go to the next step in the wizard
            return redirect(
                view_name,
                step_id=step.next_step(form).id,
            )

    else:
        # Render an empty form
        form = step.form_class()

    return render(
        request,
        step.template,
        {"form": form, "step": step},
    )
