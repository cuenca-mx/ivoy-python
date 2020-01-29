import pytest

from ivoy import Client, exc


@pytest.mark.vcr
def test_client_fail():
    client = Client('wrong', 'creds', 'for', 'ivoy', 'api', 'validation')
    try:
        client.init_tokens()
    except exc.InvalidInformation as ivoy_exc:
        assert ivoy_exc.code == -192
        assert ivoy_exc.message == 'Invalid Information Provided'
