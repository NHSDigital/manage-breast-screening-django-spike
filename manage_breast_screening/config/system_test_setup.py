import os

import pytest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import expect, sync_playwright


@pytest.mark.system
class SystemTestCase(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        super().setUpClass()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.browser.close()
        cls.playwright.stop()

    def setUp(self):
        self.page = self.browser.new_page()
        self.page.set_default_timeout(5000)

    def tearDown(self):
        self.page.close()

    def expect_validation_error(
        self, label: str, fieldset_legend: str, error_text: str, name: str | None = ""
    ):
        summary_box = self.page.locator(".nhsuk-error-summary")
        expect(summary_box).to_contain_text(error_text)

        error_link = summary_box.get_by_text(error_text)
        error_link.click()

        fieldset = self.page.locator("fieldset").filter(has_text=fieldset_legend)
        error_span = fieldset.locator("span").filter(has_text=error_text)
        expect(error_span).to_contain_text(error_text)

        if name:
            field = fieldset.get_by_label(label).and_(
                fieldset.locator(f"[name='{name}']")
            )
        else:
            field = fieldset.get_by_label(label)

        expect(field).to_be_focused()
