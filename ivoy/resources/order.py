import datetime as dt
from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List, Optional

from ..exc import NotEnoughAddresses
from .base import Resource

from ..types import (  # noqa isort:skip
    CoverageZone,
    OrderAddress,
    OrderStatus,
    Package,
    PaymentMethod,
    Vehicle,
)


@dataclass
class Order(Resource):
    """
    Based on: http://docs.ivoy.mx/express/#órdenes
    """

    _endpoint: ClassVar[str] = '/api/order'
    _response: Dict[str, Any]
    id: Optional[int]
    date_add: dt.datetime
    date_edit: dt.datetime
    discount: float
    price: float
    eta: float
    total: float
    addresses: List[OrderAddress]
    payment_method: PaymentMethod
    zone: Optional[CoverageZone]
    order_status: OrderStatus
    order_type: Optional[int]
    package_type: Optional[Package]
    payment_status: Optional[int]
    vehicle: Optional[Vehicle]

    @classmethod
    def create(
        cls,
        addresses: List[OrderAddress],
        package: Package,
        payment: PaymentMethod,
    ) -> 'Order':
        if len(addresses) < 2:
            raise NotEnoughAddresses(-111, "2 addresses minimum per order.")
        endpoint = f'{cls._endpoint}/newOrder/json/web'
        address_array = [address.to_dict() for address in addresses]
        json_data = cls._create_json(address_array, package, payment)
        resp = cls._client.put(endpoint, json=json_data)
        return cls._to_object(resp.json(), addresses)

    @classmethod
    def retrieve(cls, identity_id: str) -> 'Order':
        endpoint = f'{cls._endpoint}/getById/json/web'
        json_data = cls._update_json(identity_id)
        resp = cls._client.post(endpoint, json=json_data)
        return cls._to_object(resp.json())

    @classmethod
    def cancel(cls, identity_id: str) -> 'Order':
        endpoint = f'{cls._endpoint}/cancelOrder/json/web'
        json_data = cls._update_json(identity_id)
        resp = cls._client.put(endpoint, json=json_data)
        return cls._to_object(resp.json())

    @staticmethod
    def _to_object(
        response: dict, addresses: List[OrderAddress] = [],
    ) -> 'Order':
        data = response['data']
        if addresses == []:
            for order_addr in data['orderAddresses']:
                addresses.append(
                    OrderAddress(
                        is_pickup=order_addr['isPickup'],
                        is_source=order_addr['isSource'],
                        phone=order_addr['phone'],
                        external_number=order_addr['address'][
                            'externalNumber'
                        ],
                        latitude=order_addr['address']['latitude'],
                        longitude=order_addr['address']['longitude'],
                        neighborhood=order_addr['address']['neighborhood'],
                        street=order_addr['address']['street'],
                        zip_code=order_addr['address']['zipCode'],
                        person_approved=order_addr['personApproved'],
                        id_address=order_addr['address']['idAddress'],
                    )
                )
        return Order(
            _response=response,
            id=data['idOrder'],
            date_add=dt.datetime.fromtimestamp(data['dateAdd'] // 1000),
            date_edit=dt.datetime.fromtimestamp(data['dateEdit'] // 1000),
            discount=data['discount'],
            price=data['price'],
            eta=data['eta'],
            total=data['total'],
            addresses=addresses,
            payment_method=PaymentMethod(
                data['paymentMethod']['idPaymentMethod']
            ),
            zone=CoverageZone(data['zone']['idZone'])
            if 'zone' in data
            else None,
            order_status=OrderStatus(data['orderStatus']['idOrderStatus']),
            order_type=data['orderType']['idOrderType'],
            package_type=Package(data['packageType']['idPackageType'])
            if 'packageType' in data
            else None,
            payment_status=data['paymentStatus']['idPaymentStatus']
            if 'paymentStatus' in data
            else None,
            vehicle=Vehicle(data['vehicle']['idVehicle'])
            if 'vehicle' in data
            else None,
        )

    @staticmethod
    def _create_json(
        address_array: list, package: Package, payment: PaymentMethod,
    ) -> dict:
        json_data = dict(
            data=dict(
                bOrder=dict(
                    device='api',
                    orderType=dict(idOrderType=1),
                    packageType=dict(idPackageType=package.value),
                    paymentMethod=dict(idPaymentMethod=payment.value),
                    orderAddresses=address_array,
                )
            )
        )
        return json_data

    @staticmethod
    def _update_json(identity_id: str) -> dict:
        json_data = dict(data=dict(bOrder=dict(idOrder=identity_id)))
        return json_data
