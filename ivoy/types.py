from dataclasses import dataclass
from enum import Enum, unique
from typing import List, Optional


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


@unique
class PackageStatus(Enum):
    created = 1
    in_order = 2
    collected = 3
    ready_to_storage = 4
    ready_to_delivery = 5
    delivered = 6
    to_storage = 7
    to_next_visit = 8
    visits_done = 9
    storaged = 10
    canceled_visit = 12
    deleted = 13
    suspend_visit = 14
    returned = 15


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


@dataclass
class PackageAddress:
    external_number: str
    neighborhood: str
    street: str
    municipality: str
    state: str
    zip_code: str
    internal_number: Optional[str] = ''
    latitude: Optional[str] = ''
    longitude: Optional[str] = ''
    id: Optional[int] = None

    def to_dict(self) -> dict:
        return dict(
            externalNumber=self.external_number,
            internalNumber=self.internal_number,
            latitude=self.latitude,
            longitude=self.longitude,
            neighborhood=self.neighborhood,
            street=self.street,
            municipality=self.municipality,
            state=self.state,
            zipCode=self.zip_code,
            idAddress=self.id,
        )


@dataclass
class PackageContact:
    name: str
    phone: str
    email: str = ''
    id: Optional[int] = None

    def to_dict(self) -> dict:
        return dict(
            name=self.name,
            phone=self.phone,
            email=self.email,
            idContact=self.id,
        )


@dataclass
class PackageInfo:
    address: PackageAddress
    contact: PackageContact
    ivoy_guide: Optional[str] = None
    comment: Optional[str] = None
    guide: Optional[str] = None
    num_guides: Optional[int] = None
    guides: Optional[List[str]] = None
    package_type: Package = Package.envelope
    is_office: bool = False
    height: Optional[int] = None
    width: Optional[int] = None
    length: Optional[int] = None
    real_weight: Optional[int] = None
    id: Optional[int] = None
    price: Optional[int] = None
    status: Optional[PackageStatus] = None

    def to_dict(self) -> dict:
        data = dict(
            idPackage=self.id,
            ivoyGuide=self.ivoy_guide,
            comment=self.comment,
            guide=self.guide,
            numGuides=self.num_guides,
            guides=self.guides,
            address=self.address.to_dict(),
            contact=self.contact.to_dict(),
            packageType=dict(idPackageType=self.package_type.value),
            isOffice=self.is_office,
            height=self.height,
            width=self.width,
            length=self.length,
            realWeight=self.real_weight,
            price=self.price,
        )
        for key in list(data):
            if data[key] is None:
                del data[key]
        return data
