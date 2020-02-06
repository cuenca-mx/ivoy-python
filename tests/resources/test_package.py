import pytest

from ivoy import Client
from ivoy.types import Package, PackageAddress, PackageContact, PackageInfo


def package_info():
    contact = PackageContact(
        name='Andres Hernandez', phone='5529372492', email='andres@cuenca.com',
    )
    package_type = Package.envelope
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
    assert resp['data'][0]['idPackage']
    assert resp['data'][0]['guideIvoy']
    assert resp['data'][0]['price']
    assert Package(resp['data'][0]['packageType']['idPackageType'])


@pytest.mark.vcr
def test_package_retrieve():
    client = Client()
    resp = client.package.retrieve(40871)
    assert resp
    assert resp['data']['idPackage'] == 40871
    assert resp['data']['guideIvoy']
    assert resp['data']['price']
    assert Package(resp['data']['packageType']['idPackageType'])


@pytest.mark.vcr
def test_package_retrieve_with_filters():
    client = Client()
    resp = client.package.retrieve_from_dates(
        from_date=1580855097790, until_date=1580925884950
    )
    assert resp
    assert 0 <= len(resp['data']['packages']) <= resp['data']['elementsByPage']
    assert resp['data']['fromDate'] == 1580855097790
    assert resp['data']['untilDate'] == 1580925884950
    assert resp['data']['idClient'] == client.id_client


@pytest.mark.vcr
def test_package_delete():
    client = Client()
    resp = client.package.delete([40870])
    assert resp
    assert resp['code'] == 0
    assert resp['data'] is True
