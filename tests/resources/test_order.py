import pytest

from ivoy import Client
from ivoy.exc import IvoyException
from ivoy.resources import Order
from ivoy.types import OrderAddress, OrderStatus, Package, PaymentMethod


def order_info():
    origin = OrderAddress(
        is_pickup=1,
        is_source=1,
        person_approved='Jon Doe',
        phone='5522334455',
        id_address=None,
        external_number='36',
        internal_number=None,
        comment='N/A',
        latitude='19.4245207',
        longitude='-99.1676911',
        neighborhood='Juarez',
        street='Varsovia',
        zip_code='06600',
    )

    destiny = OrderAddress(
        is_pickup=0,
        is_source=0,
        person_approved='Lewis Hamilton',
        phone='5566778899',
        id_address=None,
        external_number='180',
        internal_number='1',
        comment='N/A',
        latitude='19.4133562',
        longitude='-99.1672142',
        neighborhood='Hipodromo',
        street='Sonora',
        zip_code='06100',
    )
    payment = PaymentMethod.credit_prepaid
    package = Package.envelope
    return dict(
        origin=origin, destiny=destiny, payment=payment, package=package
    )


@pytest.mark.vcr
def test_order_create():
    client = Client()
    info = order_info()
    order = client.order.create(
        info['origin'], info['destiny'], info['package'], info['payment']
    )
    assert order
    assert type(order) == Order
    assert order.id


@pytest.mark.vcr
def test_order_retrieve():
    client = Client()
    info = order_info()
    order_created = client.order.create(
        info['origin'], info['destiny'], info['package'], info['payment']
    )
    order = client.order.retrieve(order_created.id)
    assert order
    assert type(order) == Order
    assert order.id == order_created.id


@pytest.mark.vcr
def test_order_retrieve_fail():
    client = Client()
    order = None
    try:
        order = client.order.retrieve('wrong')
    except IvoyException as e:
        assert client
        assert e.code == -100
        assert order is None


@pytest.mark.vcr
def test_order_cancel():
    client = Client()
    info = order_info()
    order_created = client.order.create(
        info['origin'], info['destiny'], info['package'], info['payment']
    )
    order = client.order.cancel(order_created.id)
    assert order
    assert type(order) == Order
    assert order.order_status == OrderStatus.cancelled_by_customer
    assert order.id == order_created.id


@pytest.mark.vcr
def test_order_cancel_fail():
    client = Client()
    order = None
    try:
        order = client.order.cancel('wrong')
    except IvoyException as e:
        assert client
        assert e.code == -100
        assert order is None
