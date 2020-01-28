import pytest
from requests import HTTPError

from ivoy import Client, exc
from ivoy.resources import Order
from ivoy.types import OrderAddress, OrderStatus, Package, PaymentMethod


def order_info():
    origin = OrderAddress(
        is_pickup=1,
        is_source=1,
        person_approved='Jon Doe',
        phone='not a number',
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

    origin_badNumber = OrderAddress(
        is_pickup=1,
        is_source=1,
        person_approved='Jon Doe',
        phone='not a number',
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

    destiny_badNumber = OrderAddress(
        is_pickup=0,
        is_source=0,
        person_approved='Lewis Hamilton',
        phone='',
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
    bad_number_addresses = [origin_badNumber, destiny_badNumber]
    adresses = [origin, destiny]
    bad_addresses = [origin]
    payment = PaymentMethod.credit_prepaid
    package = Package.envelope

    return dict(
        adresses=adresses,
        bad_addresses=bad_addresses,
        payment=payment,
        package=package,
        bad_number_addresses=bad_number_addresses,
    )


@pytest.mark.vcr
def test_order_create():
    client = Client()
    info = order_info()
    order = client.order.create(
        info['adresses'], info['package'], info['payment']
    )
    assert order
    assert type(order) == Order
    assert order.id


@pytest.mark.vcr
def test_order_create_fail():
    client = Client()
    info = order_info()
    try:
        client.order.create(
            info['bad_addresses'], info['package'], info['payment']
        )
    except exc.NotEnoughAddresses as e:
        assert client
        assert e.code == -111


@pytest.mark.vcr
def test_order_retrieve():
    client = Client()
    info = order_info()
    order_created = client.order.create(
        info['adresses'], info['package'], info['payment']
    )
    order = client.order.retrieve(order_created.id)
    assert order
    assert type(order) == Order
    assert order.id == order_created.id


@pytest.mark.vcr
def test_order_retrieve_http_500_error():
    client = Client()
    info = order_info()

    with pytest.raises(HTTPError) as ex:
        client.order.create(info['adresses'], info['package'], info['payment'])
    assert ex.value.response.status_code == 500


@pytest.mark.vcr
def test_order_retrieve_fail():
    client = Client()
    order = None
    try:
        order = client.order.retrieve('wrong')
    except exc.IvoyException as e:
        assert client
        assert e.code == -100
        assert order is None


@pytest.mark.vcr
def test_order_cancel():
    client = Client()
    info = order_info()
    order_created = client.order.create(
        info['adresses'], info['package'], info['payment']
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
    except exc.IvoyException as e:
        assert client
        assert e.code == -100
        assert order is None


@pytest.mark.vcr
def test_order_create_bad_phone_number():
    client = Client()
    info = order_info()
    try:
        client.order.create(
            info['bad_number_addresses'], info['package'], info['payment']
        )
    except exc.InvalidPhone as e:
        assert client
        assert e.code == -101
        assert e.message == f'Invalid or incomplete Phone Number'


@pytest.mark.vcr
def test_not_available():
    client = Client()
    info = order_info()
    try:
        client.order.create(info['adresses'], info['package'], info['payment'])
    except exc.NotAvailable as e:
        assert client
        assert e.code == -160
        assert e.message == f'System Not Available, try again later'


@pytest.mark.vcr
def test_invalid_code():
    client = Client()
    info = order_info()
    try:
        client.order.create(info['adresses'], info['package'], info['payment'])
    except exc.InvalidCode as e:
        assert client
        assert e.code == -124
        assert e.message == f'This code is not valid or already used'
