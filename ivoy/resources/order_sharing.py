from dataclasses import dataclass
from typing import ClassVar

from .base import Resource


@dataclass
class OrderSharing(Resource):
    """
    This is based in iVoy App
    """

    _endpoint: ClassVar[
        str
    ] = '/v1/data/orderSharing/createSharingURL/json/web'

    id: str
    tracking_url: str

    @classmethod
    def get_tracking_url(cls, identity_id: str) -> 'OrderSharing':
        json_data = cls._json_data(identity_id)
        resp = cls._client.post(cls._endpoint, json=json_data)
        resp_json = resp.json()
        return cls(
            id=identity_id, tracking_url=resp_json['data']['trackingURL']
        )

    @staticmethod
    def _json_data(identity_id: str) -> dict:
        json_data = dict(data=dict(bOrder=dict(idOrder=identity_id)))
        return json_data
