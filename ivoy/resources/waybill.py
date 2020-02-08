from dataclasses import dataclass
from typing import ClassVar, List, Optional

from .base import Resource


@dataclass
class Waybill(Resource):
    """
    Based on: http://docs.ivoy.mx/sameday/#etiquetas
    """

    _endpoint: ClassVar[
        str
    ] = '/public/packages/getData/getMassiveTags/json/web'
    id_package_list: Optional[List[int]] = None
    guide_list: Optional[List[str]] = None
    ivoy_guide_list: Optional[List[str]] = None
    byte_content: Optional[bytes] = None

    @classmethod
    def download(
        cls,
        id_package_list: Optional[List[int]] = None,
        guide_list: Optional[List[str]] = None,
        ivoy_guide_list: Optional[List[str]] = None,
    ):
        if not any([id_package_list, guide_list, ivoy_guide_list]):
            raise ValueError("Any kind of id's are needed for waybills.")
        json_data = cls._download_json(
            id_package_list, guide_list, ivoy_guide_list
        )
        resp = cls._client.post(cls._endpoint, json=json_data)
        return cls(
            id_package_list=id_package_list,
            guide_list=guide_list,
            ivoy_guide_list=ivoy_guide_list,
            byte_content=resp.content,
        )

    @staticmethod
    def _download_json(
        id_package_list: Optional[List[int]] = None,
        guide_list: Optional[List[str]] = None,
        ivoy_guide_list: Optional[List[str]] = None,
    ) -> dict:
        json_data = dict(data=dict(packageRequest=dict()))  # type: dict
        if id_package_list:
            json_data['data']['packageRequest'].update(
                dict(idPackageList=id_package_list)
            )
        elif guide_list:
            json_data['data']['packageRequest'].update(
                dict(guideList=guide_list)
            )
        else:
            json_data['data']['packageRequest'].update(
                dict(guideIvoyList=ivoy_guide_list)
            )

        return json_data
