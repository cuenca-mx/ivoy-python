import pytest

from ivoy import Client
from ivoy.exc import IvoyException
from ivoy.resources import OrderSharing


@pytest.mark.vcr
def test_order_sharing():
    client = Client()
    order_sharing = client.order_sharing.get_tracking_url(1438597)
    assert order_sharing
    assert type(order_sharing) == OrderSharing
    assert order_sharing.id == 1438597
    assert (
        order_sharing.tracking_url
        == 'https://v2.ivoy.mx/client/app/share/MTQzODU5N2k='
    )


@pytest.mark.vcr
def test_order_sharing_fail():
    client = Client()
    order_sharing = None
    try:
        order_sharing = client.order_sharing.get_tracking_url(1437397)
    except IvoyException as e:
        assert client
        assert e.code == -283
        assert order_sharing is None
