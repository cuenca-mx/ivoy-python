import pytest

from ivoy import Client
from ivoy.resources import Waybill


@pytest.mark.vcr
def test_waybill_by_id():
    client = Client()
    resp = client.waybill.download(id_package_list=[40868])
    assert resp
    assert type(resp) == Waybill


@pytest.mark.vcr
def test_waybill_by_guide():
    client = Client()
    resp = client.waybill.download(guide_list=['000303389P000040868'])
    assert resp
    assert type(resp) == Waybill


@pytest.mark.vcr
def test_waybill_by_ivoy_guide():
    client = Client()
    resp = client.waybill.download(ivoy_guide_list=['000303389P000040868'])
    assert resp
    assert type(resp) == Waybill
