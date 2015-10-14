import json
from unittest.mock import patch

import pytest

from tululbot.utils import QuoteEngine

generic_quote_1 = (
    '--- '
    'quotes: '
    '  - q_no: 1'
    '    quote: "Kenapa kalo mau sahur tiba2 ngantuk? Karena Anda belum punya cinta yang menemani Anda sahur."'
    '    author: Anang Ferdi'
    '    author_bio: Dokter cinta veteran'
    '    tags: '
    '      - cinta'
    '      - sahur'
    '      - ramadhan'
)

generic_quote_2 = (
    '---'
    'quotes:'
    '  - q_no: 3'
    '    quote: "Cinta itu bisa dibagi dengan 0 ga sih?"'
    '    author: Adrian Nuradiansyah'
    '    author_bio: Awesome Akhi'
    '    tags: '
    '      - cinta'
    '      - geek'
    '      - matematika '
)

@pytest.fixture
def qe():
    return QuoteEngine()

def test_refresh_time(qe):
    with patch('tululbot.tils.datetime.datetime') as mock_dt:
        with patch('tululbot.utils.requests') as mock_requests:
            class FakeResponse:
                pass

            response1 = FakeResponse()
            response1.status_code = 200
            response1.text = (
                '{'
                '    "commit": {'
                '        "sha": "beefbeef"'
                '    }'
                '}'
            )
            response1.ok = True

            response2 = FakeResponse()
            response2.status_code = 200
            response2.text = (
                '<html>'
                '    <div id="mw-content-text">'
                '        <p>Snowden is former CIA employee.</p>'
                '    </div>'
                '</html>'
            )

            mock_requests.get.side_effect = {
                qe._git_branch_check_url: response1
            }

            qe.refresh_interval = 5

            mock_dt.now.return_value = datetime(2009, 1, 6, 15, 8, 30)
            qe._last_refresh = datetime(2000, 1, 6, 15, 8, 24)

            result = qe.refresh_url_if_applicable
            assert result == True
            result = qe.refresh_url_if_applicable
            assert result == False
            result = qe.refresh_url_if_applicable
            assert result == False

            qe._last_refresh = datetime(2000, 1, 6, 15, 8, 24)

            result = qe.refresh_url_if_applicable
            assert result == True
            result = qe.refresh_url_if_applicable
            assert result == False

