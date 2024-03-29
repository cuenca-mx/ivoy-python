import pytest

from ivoy import Client
from ivoy.exc import IvoyException
from ivoy.resources import CarrierLocation


@pytest.mark.vcr
def test_location_sharing_success():
    client = Client()
    location_sharing = client.carrier_location.get_location(1502057)
    assert client
    assert type(location_sharing) == CarrierLocation
    assert location_sharing.id == 1502057
    assert type(location_sharing.latitude) == float
    assert type(location_sharing.longitude) == float


@pytest.mark.vcr
def test_location_sharing_no_messenger_location():
    with pytest.raises(IvoyException):
        client = Client()
        location_sharing = client.carrier_location.get_location(9502058)
        assert client
        assert IvoyException.code == -999
        assert location_sharing is None


@pytest.mark.vcr
def test_location_sharing_failed():
    with pytest.raises(IvoyException):
        client = Client()
        location_sharing = client.carrier_location.get_location(123)
        assert client
        assert IvoyException.code == -111
        assert location_sharing is None
        assert IvoyException.message == 'Invalid Information Provided'
