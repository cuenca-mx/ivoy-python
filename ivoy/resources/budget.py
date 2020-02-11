from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List

from ..exc import NotEnoughAddresses
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
    addresses: List[OrderAddress]
    zone: CoverageZone
    package_type: Package

    @classmethod
    def create(cls, addresses: List[OrderAddress], **metadata) -> 'Budget':
        if len(addresses) < 2:
            raise NotEnoughAddresses(-111, "2 addresses minimum per budget.")
        address_array = [address.to_dict() for address in addresses]
        body = dict(data=dict(bOrder=dict(orderAddresses=address_array)))
        resp = cls._client.post(cls._endpoint, json=body)
        resp = resp.json()
        data = resp['data']
        return cls(
            _response=resp,
            distance=data['distance'],
            price=data['price'],
            eta=data['eta'],
            zone=CoverageZone(data['zone']['idZone']),
            package_type=Package(data['packageType']['idPackageType']),
            addresses=addresses,
        )
