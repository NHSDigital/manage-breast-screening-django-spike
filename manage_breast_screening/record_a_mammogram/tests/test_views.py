import pytest
from django.urls import reverse
from pytest_django.asserts import assertContains, assertRedirects

from manage_breast_screening.clinics.tests.factories import AppointmentFactory


@pytest.fixture
def appointment():
    return AppointmentFactory.create()


@pytest.mark.django_db
class TestStartScreening:
    def test_appointment_continued(self, client, appointment):
        response = client.post(
            reverse(
                "record_a_mammogram:start_screening", kwargs={"id": appointment.pk}
            ),
            {"decision": "continue"},
        )
        assertRedirects(
            response,
            reverse(
                "record_a_mammogram:ask_for_medical_information",
                kwargs={"id": appointment.pk},
            ),
        )

    def test_appointment_stopped(self, client, appointment):
        response = client.post(
            reverse(
                "record_a_mammogram:start_screening", kwargs={"id": appointment.pk}
            ),
            {"decision": "dropout"},
        )
        assertRedirects(
            response,
            reverse(
                "record_a_mammogram:appointment_cannot_go_ahead",
                kwargs={"id": appointment.pk},
            ),
        )

    def test_renders_invalid_form(self, client, appointment):
        response = client.post(
            reverse(
                "record_a_mammogram:start_screening", kwargs={"id": appointment.pk}
            ),
            {},
        )
        assertContains(response, "There is a problem")


@pytest.mark.django_db
class TestAskForMedicalInformation:
    def test_continue_to_record(self, client, appointment):
        response = client.post(
            reverse(
                "record_a_mammogram:ask_for_medical_information",
                kwargs={"id": appointment.pk},
            ),
            {"decision": "yes"},
        )
        assertRedirects(
            response,
            reverse(
                "record_a_mammogram:record_medical_information",
                kwargs={"id": appointment.pk},
            ),
        )

    def test_continue_to_imaging(self, client, appointment):
        response = client.post(
            reverse(
                "record_a_mammogram:ask_for_medical_information",
                kwargs={"id": appointment.pk},
            ),
            {"decision": "no"},
        )
        assertRedirects(
            response,
            reverse(
                "record_a_mammogram:awaiting_images",
                kwargs={"id": appointment.pk},
            ),
        )

    def test_renders_invalid_form(self, client, appointment):
        response = client.post(
            reverse(
                "record_a_mammogram:ask_for_medical_information",
                kwargs={"id": appointment.pk},
            ),
            {},
        )
        assertContains(response, "There is a problem")


@pytest.mark.django_db
class TestCheckIn:
    def test_known_redirect(self, client, appointment):
        response = client.post(
            reverse("record_a_mammogram:check_in", kwargs={"id": appointment.pk}),
            {"next": "start-screening"},
        )
        assertRedirects(
            response,
            reverse(
                "record_a_mammogram:start_screening", kwargs={"id": appointment.pk}
            ),
        )
