import pytest

from manage_breast_screening.config.system_test_setup import SystemTestCase
from manage_breast_screening.clinics.tests.factories import ClinicFactory


class TestUserViewsClinicShowPage(SystemTestCase):
    @pytest.fixture(autouse=True)
    def before(self):
        self.clinic = ClinicFactory()

    def test_user_views_clinic_show_page(self):
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
