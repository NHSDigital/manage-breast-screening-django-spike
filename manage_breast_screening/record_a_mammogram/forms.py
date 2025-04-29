from django import forms

from ..form_utils import ChoiceStep, Step, Wizard


class ScreeningAppointmentForm(forms.Form):
    next_step = forms.ChoiceField(
        choices=(
            ("continue", "Yes, go to medical information"),
            ("dropout", "No, screening cannot proceed"),
        ),
        required=True,
        widget=forms.RadioSelect(),
    )


class AskForMedicalInformation(forms.Form):
    next_step = forms.ChoiceField(
        choices=(
            ("continue", "Yes, mark incomplete sections as ‘none’ or ‘no’"),
            ("dropout", "No, screening cannot proceed"),
        ),
        required=True,
        widget=forms.RadioSelect(),
    )


class RecordMedicalInformation(forms.Form):
    next_step = forms.ChoiceField(
        choices=(
            ("continue", "Yes, go to medical information"),
            ("dropout", "No, screening cannot proceed"),
        ),
        required=True,
        widget=forms.RadioSelect(),
    )


APPOINTMENT_CANNOT_GO_AHEAD = Step(
    id="appointment-cannot-go-ahead", title="Appointment cannot go ahead"
)

AWAITING_IMAGES = Step(id="awaiting-images", title="Awaiting images")

RECORD_MEDICAL_INFORMATION = ChoiceStep(
    id="record-medical-information",
    title="Record medical information",
    form_class=RecordMedicalInformation,
    next_step_legend="Can imaging go ahead?",
    continue_step=AWAITING_IMAGES,
    continue_label="Yes, mark incomplete sections as ‘none’ or ‘no’",
    dropout_label="No, appointment needs to stop",
    dropout_step=APPOINTMENT_CANNOT_GO_AHEAD,
)

ASK_FOR_MEDICAL_INFORMATION = ChoiceStep(
    id="ask-for-medical-information",
    title="Medical information",
    form_class=AskForMedicalInformation,
    next_step_legend="Has the participant shared any relevant medical information?",
    continue_step=RECORD_MEDICAL_INFORMATION,
    dropout_step=AWAITING_IMAGES,
    continue_label="Yes",
    dropout_label="No - proceed to imaging",
)

START_SCREENING_APPOINTMENT = ChoiceStep(
    id="start-screening-appointment",
    title="Screening appointment",
    next_step_legend="Can the appointment go ahead?",
    next_step_hint="Before you proceed, check the participant’s identity and confirm that their last mammogram was more than 6 months ago.",
    form_class=ScreeningAppointmentForm,
    continue_step=ASK_FOR_MEDICAL_INFORMATION,
    dropout_step=APPOINTMENT_CANNOT_GO_AHEAD,
    continue_label="Yes, go to medical information",
    dropout_label="No, screening cannot proceed",
)

WIZARD = Wizard(START_SCREENING_APPOINTMENT)
