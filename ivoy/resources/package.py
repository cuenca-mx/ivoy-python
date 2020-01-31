from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List, Optional

from ..types import Package, PackageAddress, PackageContact
from .base import Resource


@dataclass
class Package(Resource):
    """
    Based on: http://docs.ivoy.mx/sameday/#paquetes
    """

    _endpoint: ClassVar[str] = '/public'
    _response: Dict[str, Any]
    id: Optional[int]
    id_client: Optional[int]
    id_warehouse: Optional[int]
    price: Optional[int]
    address: PackageAddress
    contact: PackageContact
    package_type: Package = Package.envelope
    comment: str = ''
    guide: str = ''
    is_office: bool = False
    num_guides: Optional[int] = None
    guides: Optional[List[str]] = None
    height: Optional[int] = None
    width: Optional[int] = None
    length: Optional[int] = None
    real_weight: Optional[int] = None

    @classmethod
    def create(cls):
        endpoint = f'{cls._endpoint}/packages/setData/newPackage/json/web'

    @classmethod
    def create(cls):
        endpoint = (
            f'{cls._endpoint}/packages/getData/getPackagesWithFilters/json/web'
        )

    @classmethod
    def retrieve(cls):
        endpoint = f'{cls._endpoint}/package/selectPackage/json/web'

    @classmethod
    def edit(cls):
        endpoint = f'{cls._endpoint}/package/editPackage/json/web'

    @classmethod
    def delete(cls, identity_id: int, id_client: int):
        endpoint = f'{cls._endpoint}/packages/setData/deletePackage/json/web'
        json_data = cls._delete_json(identity_id, id_client)
        resp = cls._client.put(endpoint, json=json_data)
        return resp

    @staticmethod
    def _create_json(identity_id: str) -> dict:
        json_data = dict(
            data=dict(
                packageRequest=dict(
                    idClient='api',
                    orderType=dict(idOrderType=1),
                    packageType=dict(idPackageType=package.value),
                    paymentMethod=dict(idPaymentMethod=payment.value),
                    orderAddresses=address_array,
                )
            )
        )
        return json_data

    @staticmethod
    def _retrieve_json(identity_id: int) -> dict:
        return dict(data=dict(bPackage=dict(idPackage=identity_id)))

    @staticmethod
    def _delete_json(identity_id: int, id_client: int) -> dict:
        return dict(
            data=dict(
                packageRequest=dict(
                    idClient=id_client,
                    packageList=[dict(idPackage=identity_id)],
                )
            )
        )
