import datetime as dt
from dataclasses import dataclass
from typing import Any, ClassVar, Dict, Optional

from ..types import OrderAddress
from .base import Resource


@dataclass
class Order(Resource):
    """
    Based on: http://docs.ivoy.mx/express/#órdenes
    """

    _endpoint: ClassVar[str] = "/api/order"
    _response: Dict[str, Any]
    id: Optional[int]
    date_add: dt.datetime
    date_edit: dt.datetime
    discount: float
    price: float
    eta: float
    total: float
    origin: OrderAddress
    destiny: OrderAddress
    payment_method: Optional[int]
    zone: Optional[int]
    order_status: Optional[int]
    order_type: Optional[int]
    package_type: Optional[int]
    payment_status: Optional[int]
    vehicle: Optional[int]

    @classmethod
    def create(cls, origin: OrderAddress, destiny: OrderAddress) -> "Order":
        endpoint = f"{cls._endpoint}/newOrder/json/web"
        json_data = cls._create_json(origin, destiny)
        resp = cls._client.put(endpoint, json=json_data)
        return cls._to_object(resp, origin, destiny)

    @classmethod
    def retrieve(cls, identity_id: str) -> "Order":
        endpoint = f"{cls._endpoint}/getById/json/web"
        json_data = cls._update_json(identity_id)
        resp = cls._client.post(endpoint, json=json_data)
        return cls._to_object(resp)

    @classmethod
    def cancel(cls, identity_id: str) -> "Order":
        endpoint = f"{cls._endpoint}/cancelOrder/json/web"
        json_data = cls._update_json(identity_id)
        resp = cls._client.put(endpoint, json=json_data)
        return cls._to_object(resp)

    @staticmethod
    def _to_object(
        response: dict,
        origin: OrderAddress = None,
        destiny: OrderAddress = None,
    ) -> "Order":
        data = response["data"]
        if origin is None:
            source_address = data["orderAddresses"][0]
            origin = OrderAddress(
                is_pickup=source_address["isPickup"],
                is_source=source_address["isSource"],
                phone=source_address["phone"],
                external_number=source_address["address"]["externalNumber"],
                latitude=source_address["address"]["latitude"],
                longitude=source_address["address"]["longitude"],
                neighborhood=source_address["address"]["neighborhood"],
                street=source_address["address"]["street"],
                zip_code=source_address["address"]["zipCode"],
                person_approved=source_address["personApproved"],
                id_address=source_address["address"]["idAddress"],
            )
        if destiny is None:
            destiny_address = data["orderAddresses"][-1]
            destiny = OrderAddress(
                is_pickup=destiny_address["isPickup"],
                is_source=destiny_address["isSource"],
                phone=destiny_address["phone"],
                external_number=destiny_address["address"]["externalNumber"],
                latitude=destiny_address["address"]["latitude"],
                longitude=destiny_address["address"]["longitude"],
                neighborhood=destiny_address["address"]["neighborhood"],
                street=destiny_address["address"]["street"],
                zip_code=destiny_address["address"]["zipCode"],
                person_approved=destiny_address["personApproved"],
                id_address=destiny_address["address"]["idAddress"],
            )
        return Order(
            _response=response,
            id=data["idOrder"],
            date_add=dt.datetime.fromtimestamp(data["dateAdd"] // 1000),
            date_edit=dt.datetime.fromtimestamp(data["dateEdit"] // 1000),
            discount=data["discount"],
            price=data["price"],
            eta=data["eta"],
            total=data["total"],
            origin=origin,
            destiny=destiny,
            payment_method=data["paymentMethod"]["idPaymentMethod"],
            zone=data["zone"]["idZone"] if "zone" in data else None,
            order_status=data["orderStatus"]["idOrderStatus"],
            order_type=data["orderType"]["idOrderType"],
            package_type=data["packageType"]["idPackageType"]
            if "packageType" in data
            else None,
            payment_status=data["paymentStatus"]["idPaymentStatus"]
            if "paymentStatus" in data
            else None,
            vehicle=data["vehicle"]["idVehicle"]
            if "vehicle" in data
            else None,
        )

    @staticmethod
    def _create_json(origin: OrderAddress, destiny: OrderAddress) -> dict:
        json_data = dict(
            data=dict(
                bOrder=dict(
                    device="api",
                    orderType=dict(idOrderType=1),
                    packageType=dict(idPackageType=1),
                    paymentMethod=dict(idPaymentMethod=4),
                    orderAddresses=[origin.to_dict(), destiny.to_dict()],
                )
            )
        )
        return json_data

    @staticmethod
    def _update_json(identity_id: str) -> dict:
        json_data = dict(data=dict(bOrder=dict(idOrder=identity_id)))
        return json_data
