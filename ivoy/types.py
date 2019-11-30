import json
from dataclasses import dataclass
from enum import Enum, unique
from typing import Optional


@unique
class CoverageZone(Enum):
    CDMX = 1
    GDL = 2


@unique
class Vehicle(Enum):
    bike_whitout_box = 1
    bike_with_box = 2
    moto_without_box = 3
    moto_box_medium = 5
    moto_box_big = 6


@unique
class Package(Enum):
    envelope = 1
    box_medium = 2
    box_big = 3


@unique
class PaymentMethod(Enum):
    credit_prepaid = 4


@unique
class OrderStatus(Enum):
    created = 2
    round_robin = 3
    available = 4
    in_process = 5
    finalized = 6
    cancelled_by_customer = 7
    cancelled_by_user = 8
    devolutino = 9
    finalized_by_absence = 10
    finalized_with_shelter = 11
    cancelled_by_user_with_collection = 12


@dataclass
class OrderAddress:
    is_pickup: int
    is_source: int
    phone: Optional[str]
    external_number: Optional[str]
    latitude: str
    longitude: str
    neighborhood: str
    street: str
    zip_code: str
    comment: str = 'N/A'
    internal_number: Optional[str] = None
    person_approved: Optional[str] = None
    id_address: Optional[int] = None

    def to_dict(self) -> dict:
        return dict(
            isPickup=self.is_pickup,
            isSource=self.is_source,
            comment=self.comment,
            personApproved=self.person_approved,
            phone=self.phone,
            address=dict(
                idAddress=self.id_address,
                externalNumber=self.external_number,
                internalNumber=self.internal_number,
                latitude=self.latitude,
                longitude=self.longitude,
                neighborhood=self.neighborhood,
                street=self.street,
                zipCode=self.zip_code,
            ),
        )

    def to_json(self) -> str:
        return json.dumps(self.to_dict())
