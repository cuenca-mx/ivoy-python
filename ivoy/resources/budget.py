import datetime as dt
from dataclasses import dataclass, field
from typing import ClassVar, List, Optional, Union

from .base import Resource


@dataclass
class Budget(Resource):
    """
    Based on: https://docs.getmati.com/#step-2-create-a-new-identity
    """

    _endpoint: ClassVar[str] = "/api/order/"

    id: str
    dateCreated: dt.datetime
    dateUpdated: dt.datetime
    alive: Optional[bool]
    status: str
    annotatedStatus: Optional[str] = None
    user: Optional[str] = None
    metadata: Union[dict, List[str]] = field(default_factory=dict)
    fullName: Optional[str] = None
    facematchScore: Optional[float] = None

    @classmethod
    def create(cls, **metadata) -> "Budget":
        endpoint = f"{cls._endpoint}newOrder/json/web"
        resp = cls._client.put(endpoint, json=dict(metadata=metadata))
        resp["id"] = resp.pop("_id")
        return cls(**resp)

    @classmethod
    def retrieve(cls, identity_id: str) -> "Budget":
        endpoint = f"{cls._endpoint}getById/json/web"
        resp = cls._client.post(endpoint)
        resp["id"] = resp.pop("_id")
        return cls(**resp)

    @classmethod
    def cancel(cls, identity_id: str) -> "Budget":
        endpoint = f"{cls._endpoint}cancelOrder/json/web"
        resp = cls._client.put(endpoint)
        resp["id"] = resp.pop("_id")
        return cls(**resp)

    def refresh(self) -> None:
        identity = self.retrieve(self.id)
        for k, v in identity.__dict__.items():
            setattr(self, k, v)
