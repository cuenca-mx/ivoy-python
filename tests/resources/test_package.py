import pytest

from ivoy import Client
from ivoy.exc import NecessaryFields
from ivoy.resources import Package
from ivoy.types import (
    Package as PackageType,
    PackageAddress,
    PackageContact,
    PackageInfo,
)


def package_info():
    contact = PackageContact(
        name='Andres Hernandez', phone='5529372492', email='andres@cuenca.com',
    )
    package_type = PackageType.envelope
    address = PackageAddress(
        external_number='27',
        neighborhood='Hipódromo',
        street='Michoacán',
        municipality='Cuauhtemoc',
        state='CDMX',
        zip_code='06100',
        internal_number='',
        latitude='19.41042803794819',
        longitude='-99.16771385476989',
    )
    info = PackageInfo(
        address=address,
        contact=contact,
        comment='Churrería El Moro',
        package_type=package_type,
        is_office=True,
    )
    return info


@pytest.mark.vcr
def test_package_create():
    client = Client()
    info = package_info()
    resp = client.package.create([info])
    assert resp
    assert type(resp) == Package
    assert resp.package_list[0].id
    assert resp.package_list[0].ivoy_guide
    assert resp.package_list[0].price
    assert type(resp.package_list[0].package_type) == PackageType


@pytest.mark.vcr
def test_package_retrieve():
    client = Client()
    resp = client.package.retrieve(40871)
    assert resp
    assert type(resp) == Package
    assert resp.package_list[0].id == 40871
    assert resp.package_list[0].ivoy_guide
    assert resp.package_list[0].price
    assert type(resp.package_list[0].package_type) == PackageType


@pytest.mark.vcr
def test_package_retrieve_with_filters():
    client = Client()
    resp = client.package.retrieve_from_dates(
        from_date=1580855097790, until_date=1580925884950
    )
    assert resp
    assert type(resp) == Package
    num_packages = len(resp._response['data']['packages'])
    max_page = resp._response['data']['elementsByPage']
    assert 0 <= num_packages <= max_page
    assert len(resp.package_list) == num_packages
    assert resp._response['data']['fromDate'] == 1580855097790
    assert resp._response['data']['untilDate'] == 1580925884950
    assert resp._response['data']['idClient'] == client.id_client


def test_package_update_without_necessary_fields():
    client = Client()
    info = package_info()
    info.ivoy_guide = '000303389P000040874'
    info.id = 40874
    info.contact.id = 687452
    info.address.id = 303421
    info.comment = 'EDITADISIMA'
    try:
        client.package.update(info)
    except NecessaryFields as e:
        assert e.code == -111


@pytest.mark.vcr
def test_package_update():
    client = Client()
    info = package_info()
    info.ivoy_guide = '000303389P000040874'
    info.guide = '000303389P000040874'
    info.id = 40874
    info.contact.id = 687452
    info.address.id = 303421
    info.comment = 'EDITADISIMA'
    resp = client.package.update(info)
    assert resp
    assert type(resp) == Package
    assert resp.package_list[0].id
    assert resp.package_list[0].ivoy_guide
    assert resp.package_list[0].price
    assert type(resp.package_list[0].package_type) == PackageType


@pytest.mark.vcr
def test_package_delete():
    client = Client()
    resp = client.package.delete([40870])
    assert resp
    assert resp['code'] == 0
    assert resp['data'] is True


def test_to_object_wrong_comes_from():
    client = Client()
    info = package_info()
    try:
        client.package._to_object(info.to_dict(), comes_from='wrong')
    except ValueError:
        pass
    else:
        assert False
