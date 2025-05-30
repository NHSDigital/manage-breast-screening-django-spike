import pytest

from ..acessibility import exclude_axe_targets, exclude_axe_violations


@pytest.fixture
def axe_response():
    return {
        "violations": [
            {
                "id": "link-name",
                "impact": "serious",
                "nodes": [
                    {
                        "impact": "serious",
                        "html": '<a href="">\n                </a>',
                        "target": [
                            '.nhsuk-summary-list__row:nth-child(1) > .nhsuk-summary-list__actions > a[href=""]'
                        ],
                        "failureSummary": "Fix all of the following:\n  Element is in tab order and does not have accessible text\n\nFix any of the following:\n  Element does not have text that is visible to screen readers\n  aria-label attribute does not exist or is empty\n  aria-labelledby attribute does not exist, references elements that do not exist or references elements that are empty\n  Element has no title attribute",
                    },
                    {
                        "impact": "serious",
                        "html": '<a href="">\n                </a>',
                        "target": [
                            '.nhsuk-summary-list__row:nth-child(2) > .nhsuk-summary-list__actions > a[href=""]'
                        ],
                        "failureSummary": "Fix all of the following:\n  Element is in tab order and does not have accessible text\n\nFix any of the following:\n  Element does not have text that is visible to screen readers\n  aria-label attribute does not exist or is empty\n  aria-labelledby attribute does not exist, references elements that do not exist or references elements that are empty\n  Element has no title attribute",
                    },
                ],
            }
        ],
    }


def test_filter_by_id(axe_response):
    exclude_axe_violations(axe_response, ["link-name"])
    assert len(axe_response["violations"]) == 0


def test_filter_by_target(axe_response):
    exclude_axe_targets(
        axe_response,
        [
            '.nhsuk-summary-list__row:nth-child(1) > .nhsuk-summary-list__actions > a[href=""]'
        ],
    )
    assert len(axe_response["violations"]) == 1
    assert len(axe_response["violations"][0]["nodes"]) == 1
