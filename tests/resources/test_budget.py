import pytest

from ivoy import Client
from ivoy.resources import Budget
from ivoy.types import OrderAddress


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
    return dict(origin=origin, destiny=destiny)


@pytest.mark.vcr
def test_budget_create():
    client = Client()
    info = order_info()
    budget = client.budget.create(info['origin'], info['destiny'])
    assert budget
    assert type(budget) == Budget
    assert budget.price
