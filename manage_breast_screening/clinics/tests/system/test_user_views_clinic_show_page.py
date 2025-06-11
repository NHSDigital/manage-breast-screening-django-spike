import re
import pytest

from datetime import datetime, timezone
from django.urls import reverse
from playwright.sync_api import expect

from manage_breast_screening.participants.models import Appointment
from manage_breast_screening.core.system_test_setup import SystemTestCase
from manage_breast_screening.participants.tests.factories import AppointmentFactory
from manage_breast_screening.clinics.tests.factories import ClinicFactory


class TestUserViewsClinicShowPage(SystemTestCase):
    @pytest.fixture(autouse=True)
    def before(self):
        today = datetime.now(timezone.utc).replace(hour=9, minute=0)
        self.clinic = ClinicFactory(starts_at=today, setting__name="West London BSS")

    def test_user_views_clinic_show_page(self):
        self.given_there_are_appointments()
        self.given_i_am_on_the_clinic_list()
        self.when_i_click_on_the_clinic()
        self.then_i_should_see_the_clinic_show_page()
        self.and_i_can_see_remaining_appointments()

        self.when_i_click_on_checked_in()
        self.then_i_can_see_checked_in_appointments()
        self.when_i_click_on_complete()
        self.then_i_can_see_completed_appointments()
        self.when_i_click_on_all()
        self.then_i_can_see_all_appointments()

        self.when_i_check_in_an_appointment()
        self.then_the_appointment_is_checked_in()

    def given_there_are_appointments(self):
        AppointmentFactory(
            clinic_slot__clinic=self.clinic,
            clinic_slot__starts_at=datetime.now(timezone.utc).replace(hour=9, minute=0),
            status=Appointment.Status.CONFIRMED,
        )
        AppointmentFactory(
            clinic_slot__clinic=self.clinic,
            clinic_slot__starts_at=datetime.now(timezone.utc).replace(hour=9, minute=0),
            status=Appointment.Status.CHECKED_IN,
        )
        AppointmentFactory(
            clinic_slot__clinic=self.clinic,
            clinic_slot__starts_at=datetime.now(timezone.utc).replace(hour=9, minute=0),
            status=Appointment.Status.SCREENED,
        )

    def given_i_am_on_the_clinic_list(self):
        self.page.goto(self.live_server_url + reverse("clinics:index"))

    def when_i_click_on_the_clinic(self):
        self.page.get_by_role("link", name="West London BSS").click()

    def then_i_should_see_the_clinic_show_page(self):
        expect(self.page).to_have_url(re.compile(f"/clinics/{self.clinic.id}"))
        heading = self.page.get_by_role("heading", level=1)
        expect(heading).to_contain_text("West London BSS")
        expect(heading).to_contain_text(self.clinic.get_risk_type_display())

    def and_i_can_see_remaining_appointments(self):
        remaining_link = self.page.get_by_role("link", name=re.compile("Remaining"))
        count_span = remaining_link.locator(".app-count")
        expect(count_span).to_contain_text("2")
