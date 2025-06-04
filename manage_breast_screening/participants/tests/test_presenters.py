from unittest.mock import MagicMock

import pytest

from manage_breast_screening.participants.presenters import ParticipantPresenter

from ..models import Participant


class TestParticipantPresenter:
    @pytest.fixture
    def mock_participant(self):
        mock = MagicMock(spec=Participant)
        mock.nhs_number = "99900900829"
        return mock

    @pytest.mark.parametrize(
        "category, formatted",
        [
            (
                "Black, African, Caribbean or Black British",
                "Black, African, Caribbean or Black British",
            ),
            (None, None),
            ("Any other", "any other"),
        ],
    )
    def test_ethnic_group_category(self, mock_participant, category, formatted):
        mock_participant.ethnic_group_category.return_value = category
        result = ParticipantPresenter(mock_participant)
        assert result.ethnic_group_category == formatted
