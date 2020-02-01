from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List, Optional

from ..types import PackageInfo
from .base import Resource


@dataclass
class Package(Resource):
    """
    Based on: http://docs.ivoy.mx/sameday/#paquetes
    """

    _endpoint: ClassVar[str] = '/public'
    _response: Dict[str, Any]
    id_client: Optional[int]
    id_warehouse: Optional[int]
    package_list: List[PackageInfo]

    @classmethod
    def create(
        cls, id_client: int, id_warehouse: int, package_list: List[PackageInfo]
    ):
        endpoint = f'{cls._endpoint}/packages/setData/newPackage/json/web'
        json_data = cls._create_json(id_client, id_warehouse, package_list)
        resp = cls._client.put(endpoint, json=json_data)
        return resp

    @classmethod
    def retrieve_from_dates(
        cls,
        start_page: int = 1,
        elements_by_page: int = 10,
        from_date: int = None,
        until_date: int = None,
    ):
        endpoint = (
            f'{cls._endpoint}/packages/getData/getPackagesWithFilters/json/web'
        )
        json_data = cls._retrieve_json_with_filters(
            start_page, elements_by_page, from_date, until_date
        )
        resp = cls._client.post(endpoint, json=json_data)
        return resp

    @classmethod
    def retrieve(cls, identity_id: int):
        endpoint = f'{cls._endpoint}/package/selectPackage/json/web'
        json_data = cls._retrieve_json(identity_id)
        resp = cls._client.post(endpoint, json=json_data)
        return resp

    @classmethod
    def edit(cls):
        endpoint = f'{cls._endpoint}/package/editPackage/json/web'
        resp = cls._client.put(endpoint, json=json_data)
        return resp

    @classmethod
    def delete(cls, identity_ids: List[int], id_client: int):
        endpoint = f'{cls._endpoint}/packages/setData/deletePackage/json/web'
        json_data = cls._delete_json(identity_id, id_client)
        resp = cls._client.put(endpoint, json=json_data)
        return resp

    @staticmethod
    def _create_json(
        id_client: int, id_warehouse: int, package_list: List[PackageInfo]
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
        start_page: int,
        elements_by_page: int,
        from_date: Optional[int],
        until_date: Optional[int],
    ) -> dict:
        package_request = dict(
            startPage=start_page, elementsByPage=elements_by_page,
        )
        if from_date:
            package_request.update(dict(fromDate=from_date))
        if until_date:
            package_request.update(dict(fromDate=until_date))
        json_data = dict(data=dict(packageRequest=package_request))
        return json_data

    @staticmethod
    def _retrieve_json(identity_id: int) -> dict:
        return dict(data=dict(bPackage=dict(idPackage=identity_id)))

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
