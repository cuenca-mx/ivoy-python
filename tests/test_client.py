import pytest

from ivoy import Client
from ivoy.exc import IvoyException
from ivoy.resources import Budget, LocationSharing, Order, OrderSharing


@pytest.mark.vcr
def test_client():
    client = Client()
    assert client
    assert client.budget == Budget
    assert client.order == Order
    assert client.order_sharing == OrderSharing
    assert client.location_sharing == LocationSharing


@pytest.mark.vcr
def test_client_fail():
    try:
        Client('wrong', 'creds', 'for', 'ivoy', 'api', 'validation')
    except IvoyException as ivoy_exc:
        assert ivoy_exc.code == -192
