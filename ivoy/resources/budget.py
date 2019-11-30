from dataclasses import dataclass
from typing import Any, ClassVar, Dict

from ..types import CoverageZone, OrderAddress, Package
from .base import Resource


@dataclass
class Budget(Resource):
    """
    Based on: http://docs.ivoy.mx/express/#cotización
    """

    _endpoint: ClassVar[str] = '/api/order/validZipCode/json/web'
    _response: Dict[str, Any]
    distance: float
    price: float
    eta: float
    origin: OrderAddress
    destiny: OrderAddress
    zone: CoverageZone
    package_type: Package

    @classmethod
    def create(
        cls, origin: OrderAddress, destiny: OrderAddress, **metadata
    ) -> 'Budget':
        body = dict(
            data=dict(
                bOrder=dict(
                    orderAddresses=[origin.to_dict(), destiny.to_dict()]
                )
            )
        )
        resp = cls._client.post(cls._endpoint, json=body)
        data = resp['data']
        return cls(
            _response=resp,
            distance=data['distance'],
            price=data['price'],
            eta=data['eta'],
            zone=CoverageZone(data['zone']['idZone']),
            package_type=Package(data['packageType']['idPackageType']),
            origin=origin,
            destiny=destiny,
        )
