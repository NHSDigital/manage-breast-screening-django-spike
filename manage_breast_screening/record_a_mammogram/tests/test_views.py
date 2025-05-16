import pytest
from django.urls import reverse
from pytest_django.asserts import assertContains, assertRedirects

from manage_breast_screening.clinics.tests.factories import AppointmentFactory


@pytest.mark.django_db
class TestStartScreening:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.appointment = AppointmentFactory.create()

    def test_appointment_continued(self, client):
        response = client.post(
            reverse(
                "record_a_mammogram:start_screening", kwargs={"id": self.appointment.pk}
            ),
            {"decision": "continue"},
        )
        assertRedirects(
            response,
            reverse(
                "record_a_mammogram:ask_for_medical_information",
                kwargs={"id": self.appointment.pk},
            ),
        )

    def test_appointment_stopped(self, client):
        response = client.post(
            reverse(
                "record_a_mammogram:start_screening", kwargs={"id": self.appointment.pk}
            ),
            {"decision": "dropout"},
        )
        assertRedirects(
            response,
            reverse(
                "record_a_mammogram:appointment_cannot_go_ahead",
                kwargs={"id": self.appointment.pk},
            ),
        )

    def test_renders_invalid_form(self, client):
        response = client.post(
            reverse(
                "record_a_mammogram:start_screening", kwargs={"id": self.appointment.pk}
            ),
            {},
        )
        assertContains(response, "There is a problem")


@pytest.mark.django_db
class TestCheckIn:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.appointment = AppointmentFactory.create()

    def test_known_redirect(self, client):
        response = client.post(
            reverse("record_a_mammogram:check_in", kwargs={"id": self.appointment.pk}),
            {"next": "start-screening"},
        )
        assertRedirects(
            response,
            reverse(
                "record_a_mammogram:start_screening", kwargs={"id": self.appointment.pk}
            ),
        )
