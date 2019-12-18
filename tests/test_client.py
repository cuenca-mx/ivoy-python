import pytest

from ivoy import Client
from ivoy.exc import IvoyException


@pytest.mark.vcr
def test_client_fail():
    client = Client('wrong', 'creds', 'for', 'ivoy', 'api', 'validation')
    try:
        client.init_tokens()
    except IvoyException as ivoy_exc:
        assert ivoy_exc.code == -192
