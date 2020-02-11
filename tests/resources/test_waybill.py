import pytest

from ivoy import Client
from ivoy.resources import Waybill


@pytest.mark.vcr
def test_waybill_by_id():
    client = Client()
    resp = client.waybill.download(id_package_list=[40868])
    assert resp
    assert type(resp) == Waybill
    assert resp.id_package_list == [40868]
    assert resp.byte_content


@pytest.mark.vcr
def test_waybill_by_guide():
    client = Client()
    resp = client.waybill.download(guide_list=['000303389P000040868'])
    assert resp
    assert type(resp) == Waybill
    assert resp.guide_list == ['000303389P000040868']
    assert resp.byte_content


@pytest.mark.vcr
def test_waybill_by_ivoy_guide():
    client = Client()
    resp = client.waybill.download(ivoy_guide_list=['000303389P000040868'])
    assert resp
    assert type(resp) == Waybill
    assert resp.ivoy_guide_list == ['000303389P000040868']
    assert resp.byte_content


def test_waybill_no_info():
    client = Client()
    try:
        client.waybill.download()
    except ValueError:
        pass
    else:
        assert False
