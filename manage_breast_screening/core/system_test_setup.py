import os

import pytest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import expect, sync_playwright

from .utils.acessibility import AxeAdapter


@pytest.mark.system
class SystemTestCase(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        super().setUpClass()
        cls.playwright = sync_playwright().start()
        is_headless = os.environ.get("HEADLESS", "1") == "1"
        cls.browser = cls.playwright.chromium.launch(headless=is_headless)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.browser.close()
        cls.playwright.stop()

    def setUp(self):
        self.page = self.browser.new_page()
        self.page.set_default_timeout(5000)
        self.axe = AxeAdapter(self.page)

    def tearDown(self):
        self.page.close()

    def expect_validation_error(
        self,
        error_text: str,
        fieldset_legend: str,
        field_label: str,
        field_name: str | None = "",
    ):
        summary_box = self.page.locator(".nhsuk-error-summary")
        expect(summary_box).to_contain_text(error_text)

        error_link = summary_box.get_by_text(error_text)
        error_link.click()

        fieldset = self.page.locator("fieldset").filter(has_text=fieldset_legend)
        error_span = fieldset.locator("span").filter(has_text=error_text)
        expect(error_span).to_contain_text(error_text)

        if field_name:
            field = fieldset.get_by_label(field_label).and_(
                fieldset.locator(f"[name='{field_name}']")
            )
        else:
            field = fieldset.get_by_label(field_label)

        expect(field).to_be_focused()

    def then_the_accessibility_baseline_is_met(self):
        """
        Check there are no Axe violations
        """
        results = self.axe.run()
        self.assertEqual(results.violations_count, 0, results.generate_report())
