from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List, Optional

from ..exc import NecessaryFields
from ..types import (
    Package as PackageType,
    PackageAddress,
    PackageContact,
    PackageInfo,
    PackageStatus,
)
from .base import Resource


@dataclass
class Package(Resource):
    """
    Based on: http://docs.ivoy.mx/sameday/#paquetes
    """

    _endpoint: ClassVar[str] = '/public'
    _response: Dict[str, Any]
    package_list: List[PackageInfo]

    @classmethod
    def create(cls, package_list: List[PackageInfo], id_warehouse: int = None):
        id_client = cls._client.id_client
        endpoint = f'{cls._endpoint}/packages/setData/newPackage/json/web'
        json_data = cls._create_json(package_list, id_client, id_warehouse)
        resp = cls._client.put(endpoint, json=json_data)
        return cls._to_object(resp.json(), comes_from='create/edit')

    @classmethod
    def retrieve_from_dates(
        cls,
        start_page: int = 1,
        elements_by_page: int = 10,
        from_date: int = None,
        until_date: int = None,
    ):
        id_client = cls._client.id_client
        endpoint = (
            f'{cls._endpoint}/packages/getData/getPackagesWithFilters/json/web'
        )
        json_data = cls._retrieve_json_with_filters(
            id_client, start_page, elements_by_page, from_date, until_date
        )
        resp = cls._client.post(endpoint, json=json_data)
        return cls._to_object(resp.json(), comes_from='filters')

    @classmethod
    def retrieve(cls, identity_id: int):
        endpoint = f'{cls._endpoint}/package/selectPackage/json/web'
        json_data = cls._retrieve_json(identity_id)
        resp = cls._client.post(endpoint, json=json_data)
        return cls._to_object(resp.json(), comes_from='retrieve')

    @classmethod
    def update(cls, package_info: PackageInfo):
        id_client = cls._client.id_client
        endpoint = f'{cls._endpoint}/package/editPackage/json/web'
        necessary_values = [
            package_info.id,
            package_info.guide,
            package_info.ivoy_guide,
        ]
        if not all(necessary_values):
            raise NecessaryFields(-111, 'Values needed to update package')
        json_data = cls._update_json(id_client, package_info)
        resp = cls._client.put(endpoint, json=json_data)
        return cls._to_object(resp.json(), comes_from='create/edit')

    @classmethod
    def delete(cls, identity_ids: List[int]):
        id_client = cls._client.id_client
        endpoint = f'{cls._endpoint}/packages/setData/deletePackage/json/web'
        json_data = cls._delete_json(identity_ids, id_client)
        resp = cls._client.put(endpoint, json=json_data)
        return resp.json()

    @staticmethod
    def _create_json(
        package_list: List[PackageInfo],
        id_client: int = None,
        id_warehouse: int = None,
    ) -> dict:
        json_data = dict(
            data=dict(
                packageRequest=dict(
                    idClient=id_client,
                    idClientWarehouse=id_warehouse,
                    packageList=[item.to_dict() for item in package_list],
                )
            )
        )
        return json_data

    @staticmethod
    def _retrieve_json_with_filters(
        id_client: int,
        start_page: int,
        elements_by_page: int,
        from_date: Optional[int],
        until_date: Optional[int],
    ) -> dict:
        package_request = dict(
            idClient=id_client,
            startPage=start_page,
            elementsByPage=elements_by_page,
        )
        if from_date:
            package_request.update(dict(fromDate=from_date))
        if until_date:
            package_request.update(dict(untilDate=until_date))
        json_data = dict(data=dict(packageRequest=package_request))
        return json_data

    @staticmethod
    def _retrieve_json(identity_id: int) -> dict:
        return dict(data=dict(bPackage=dict(idPackage=identity_id)))

    @staticmethod
    def _update_json(id_client: int, package_info: PackageInfo) -> dict:
        json_data = dict(data=dict(bPackage=package_info.to_dict()))
        json_data['data']['bPackage']['client'] = dict(idClient=id_client)
        return json_data

    @staticmethod
    def _delete_json(identity_ids: List[int], id_client: int) -> dict:
        return dict(
            data=dict(
                packageRequest=dict(
                    idClient=id_client,
                    packageList=[
                        dict(idPackage=identity_id)
                        for identity_id in identity_ids
                    ],
                )
            )
        )

    @staticmethod
    def _to_object(
        response: dict, comes_from: str = 'create/edit',
    ) -> 'Package':
        packages = list()
        if comes_from == 'filters':
            data = response['data']['packages']
            for package in data:
                full_address = package['address'].split(',')
                street_info = (
                    full_address[0].split('int')[0].strip().split(' ')
                )
                street = ' '.join(street_info[:-1])
                external_number = street_info[-1]
                address = PackageAddress(
                    id=package['idAddress'],
                    external_number=external_number,
                    neighborhood=full_address[1].strip(),
                    street=street,
                    municipality=package['municipality'],
                    state=full_address[-1].strip(),
                    zip_code=package['zipCode'],
                    internal_number=package.get('internalNumber', ''),
                    latitude=package.get('latitude', ''),
                    longitude=package.get('longitude', ''),
                )
                contact = PackageContact(
                    name=package['contact'],
                    phone=package['phoneContact'],
                    email=package['emailContact'],
                )
                packages.append(
                    PackageInfo(
                        id=package['idPackage'],
                        comment=package['comment'],
                        address=address,
                        contact=contact,
                        status=PackageStatus(package['idPackageStatus']),
                        ivoy_guide=package['guideIvoy'],
                        guide=package['guide'],
                        is_office=package['office'],
                        height=package['height'],
                        width=package['width'],
                        length=package['length'],
                        real_weight=package['realWeight'],
                    )
                )
        else:
            if comes_from == 'create/edit':
                data = response['data']
            elif comes_from == 'retrieve':
                data = [response['data']]
            else:
                raise ValueError(f'{comes_from} is not valid')

            for package in data:
                data_address = package['address']
                address = PackageAddress(
                    id=data_address['idAddress'],
                    external_number=data_address['externalNumber'],
                    neighborhood=data_address['neighborhood'],
                    street=data_address['street'],
                    municipality=data_address['municipality'],
                    state=data_address['state'],
                    zip_code=data_address['zipCode'],
                    internal_number=data_address.get('internalNumber', ''),
                    latitude=data_address['latitude'],
                    longitude=data_address['longitude'],
                )
                data_contact = package['contact']
                contact = PackageContact(
                    id=data_contact['idContact'],
                    name=data_contact['name'],
                    phone=data_contact['phone'],
                    email=data_contact['email'],
                )
                packages.append(
                    PackageInfo(
                        id=package['idPackage'],
                        comment=package['comment'],
                        price=package['price'],
                        address=address,
                        contact=contact,
                        package_type=PackageType(
                            package['packageType']['idPackageType']
                        ),
                        status=PackageStatus(
                            package['packageStatus']['idPackageStatus']
                        ),
                        ivoy_guide=package['guideIvoy'],
                        guide=package['guide'],
                        is_office=package['isOffice'],
                        height=package['height'],
                        width=package['width'],
                        length=package['length'],
                        real_weight=package['realWeight'],
                    )
                )
        return Package(_response=response, package_list=packages,)
