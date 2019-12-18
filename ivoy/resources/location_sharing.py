from dataclasses import dataclass
from typing import ClassVar

from .base import Resource


@dataclass
class LocationSharing(Resource):

    _endpoint: ClassVar[str] = '/api/orderSharing/getOrderSharing/json/web'

    id: str
    latitude: float
    longitude: float

    @classmethod
    def get_location(cls, order_id: str) -> 'LocationSharing':
        json_data = dict(data=dict(bOrder=dict(idOrder=order_id)))
        resp = cls._client.post(cls._endpoint, json=json_data)
        return cls(
            id=order_id,
            latitude=resp['data']['messengerLocation']['latitude'],
            longitude=resp['data']['messengerLocation']['longitude'],
        )
