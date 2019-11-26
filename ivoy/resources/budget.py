from dataclasses import dataclass
from typing import Any, ClassVar, Dict

from ..types import CoverageZone, OrderAddress, Package, PaymentMethod, Vehicle
from .base import Resource


@dataclass
class Budget(Resource):
    """
    Based on: http://docs.ivoy.mx/express/#cotización
    """

    _endpoint: ClassVar[str] = "/api/order/validZipCode/json/web"
    _response: Dict[str, Any]
    distance: float
    price: float
    eta: float
    origin: OrderAddress
    destiny: OrderAddress
    zone: CoverageZone
    order_type: Vehicle
    package_type: Package
    payment_status: PaymentMethod

    @classmethod
    def create(
        cls, origin: OrderAddress, destiny: OrderAddress, **metadata
    ) -> "Budget":
        body = dict(
            data=dict(
                bOrder=dict(
                    orderAddresses=[origin.to_dict(), destiny.to_dict()]
                )
            )
        )
        resp = cls._client.put(cls._endpoint, json=body)
        data = resp["data"]
        return cls(
            _response=resp,
            distance=data["distance"],
            price=data["price"],
            eta=data["eta"],
            zone=data["zone"]["idZone"],
            order_type=data["orderType"]["idOrderType"],
            package_type=data["packageType"]["idPackageType"],
            payment_status=data["paymentStatus"]["idPaymentStatus"],
            origin=origin,
            destiny=destiny,
        )
