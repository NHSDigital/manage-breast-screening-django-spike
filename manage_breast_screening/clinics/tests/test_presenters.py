from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest

from manage_breast_screening.clinics.presenters import (
    ClinicPresenter,
    AppointmentListPresenter,
)

from manage_breast_screening.clinics.tests.factories import ClinicSlotFactory
from manage_breast_screening.core.utils.date_formatting import format_time
from manage_breast_screening.participants.tests.factories import AppointmentFactory

from ..models import Clinic


@pytest.fixture
def mock_clinic():
    mock = MagicMock(spec=Clinic)

    mock.starts_at = datetime(2025, 1, 1, 9)
    mock.session_type.return_value = "All day"
    mock.clinic_slots.count.return_value = 10
    mock.setting.name = "Test setting"
    mock.time_range.return_value = {
        "start_time": datetime(2025, 1, 1, 9),
        "end_time": datetime(2025, 1, 1, 15),
    }
    mock.get_type_display.return_value = "Screening"
    mock.get_risk_type_display.return_value = "Routine"

    return mock


def test_clinic_presenter(mock_clinic):
    presenter = ClinicPresenter(mock_clinic)

    assert presenter.starts_at == "1 January 2025"
    assert presenter.session_type == "All day"
    assert presenter.number_of_slots == 10
    assert presenter.location_name == "Test setting"
    assert presenter.time_range == "9am to 3pm"
    assert presenter.type == "Screening"
    assert presenter.risk_type == "Routine"


@pytest.mark.django_db
def test_appointment_list_presenter_sorts_by_start_time():
    appointment1 = AppointmentFactory(
        clinic_slot=ClinicSlotFactory(
            starts_at=datetime(2025, 1, 1, 13, 0, tzinfo=timezone.utc)  # 1pm
        )
    )
    appointment2 = AppointmentFactory(
        clinic_slot=ClinicSlotFactory(
            starts_at=datetime(2025, 1, 1, 9, 0, tzinfo=timezone.utc)  # 9am
        )
    )
    appointment3 = AppointmentFactory(
        clinic_slot=ClinicSlotFactory(
            starts_at=datetime(2025, 1, 1, 11, 30, tzinfo=timezone.utc)  # 11:30am
        )
    )

    presenter = AppointmentListPresenter(
        [appointment1, appointment2, appointment3], "all", {}
    )

    sorted_times = [
        appointment.clinic_slot.starts_at for appointment in presenter.appointments
    ]

    assert sorted_times == [
        format_time(datetime(2025, 1, 1, 9, 0, tzinfo=timezone.utc)),  # 9am
        format_time(datetime(2025, 1, 1, 11, 30, tzinfo=timezone.utc)),  # 11:30am
        format_time(datetime(2025, 1, 1, 13, 0, tzinfo=timezone.utc)),  # 1pm
    ]
