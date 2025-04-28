from manage_breast_screening.form_utils import ChoiceStep
from manage_breast_screening.record_a_mammogram.forms import (
    APPOINTMENT_CANNOT_GO_AHEAD,
    ASK_FOR_MEDICAL_INFORMATION,
    AWAITING_IMAGES,
    RECORD_MEDICAL_INFORMATION,
    START_SCREENING_APPOINTMENT,
    ScreeningAppointmentForm,
)


def test_step_linkage():
    assert isinstance(START_SCREENING_APPOINTMENT, ChoiceStep)

    continue_form = ScreeningAppointmentForm({"next_step": True})
    assert continue_form.is_valid(), continue_form.errors
    assert (
        START_SCREENING_APPOINTMENT.next_step(continue_form)
        == ASK_FOR_MEDICAL_INFORMATION
    )

    dropout_form = ScreeningAppointmentForm({"next_step": False})
    assert dropout_form.is_valid(), dropout_form.errors
    assert (
        START_SCREENING_APPOINTMENT.next_step(dropout_form)
        == APPOINTMENT_CANNOT_GO_AHEAD
    )
