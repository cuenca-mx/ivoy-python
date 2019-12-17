import pytest

from ivoy import Client
from ivoy.exc import IvoyException
from ivoy.resources import LocationSharing


@pytest.mark.vcr
def test_location_sharing_success():
    client = Client()
    location_sharing = client.location_sharing.get_location("$ORDER_ID")
    assert type(location_sharing) == LocationSharing
    assert location_sharing.id == "$ORDER_ID"
    assert type(location_sharing.location_points) == list
    assert type(location_sharing.messengerLocation) == dict
    assert type(location_sharing.clientName) == str


@pytest.mark.vcr
def test_location_sharing_failed():
    client = Client()
    location_sharing = None
    try:
        location_sharing = client.location_sharing.get_location("$ORDER_ID")
    except IvoyException as e:
        assert client
        assert e.code == -283
        assert location_sharing is None
