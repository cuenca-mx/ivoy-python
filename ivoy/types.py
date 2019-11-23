import json

from dataclasses import dataclass, field
from enum import Enum, unique
from typing import BinaryIO, Dict, List, Optional, Union


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
    person_approved: Optional[str] = None
    phone: Optional[str] = None
    id_address: Optional[int] = None
    external_number: Optional[str] = None
    internal_number: Optional[str] = None
    comment: str = "N/A"
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    neighborhood: Optional[str] = None
    street: Optional[str] = None
    zip_code: Optional[str] = None

    def to_dict(self) -> dict:
        return dict(
            isPickup = is_pickup,
            isSource = is_source,
            comment = comment,
            personApproved = person_approved,
            phone = phone,
            address = dict(
                idAddress = id_address,
                externalNumber = external_number,
                internalNumber = internal_number,
                latitude = latitude,
                longitude = longitude,
                neighborhood = neighborhood,
                street = street,
                zipCode = zip_code
            )
        )

    def to_json(self) -> str:
        return json.dumps(self.to_dict())
    