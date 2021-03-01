from dataclasses import dataclass
from typing import ClassVar

from ivoy.exc import raise_ivoy_exception

from .base import Resource


@dataclass
class CarrierLocation(Resource):

    _endpoint: ClassVar[
        str
    ] = '/play/data/rest/orderSharing/getOrderSharing/json/web'

    id: str
    latitude: float
    longitude: float

    @classmethod
    def get_location(cls, order_id: str) -> 'CarrierLocation':
        json_data = dict(data=dict(bOrder=dict(idOrder=order_id)))
        resp = cls._client.post(cls._endpoint, json=json_data)
        resp_json = resp.json()
        try:
            messenger_location = resp_json['data']['messengerLocation']
        except KeyError as e:
            raise_ivoy_exception(-999, str(e))
        return cls(
            id=order_id,
            latitude=messenger_location['latitude'],
            longitude=messenger_location['longitude'],
        )
