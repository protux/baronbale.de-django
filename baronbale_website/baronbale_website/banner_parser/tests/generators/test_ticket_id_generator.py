from unittest import TestCase
from unittest.mock import (
    MagicMock,
    patch,
)

from baronbale_website.banner_parser.generators import ticket_id_generator


class TestTicketIdGenerator(TestCase):
    @patch(
        "baronbale_website.banner_parser.generators.ticket_id_generator.secrets.token_hex"
    )
    def test_ticket_is_separated_by_dashes(self, mock_token_hex: MagicMock) -> None:
        raw_ticket_id = "1111222233334444"
        mock_token_hex.return_value = raw_ticket_id

        actual_ticket_id = ticket_id_generator.generate_ticket_id()

        expected_ticket_id = "1111-2222-3333-4444"
        self.assertEqual(expected_ticket_id, actual_ticket_id)
