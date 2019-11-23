import datetime as dt
from dataclasses import dataclass, field
from typing import ClassVar, List, Optional, Union

from .base import Resource


@dataclass
class OrderSharing(Resource):
    """
    This is based in iVoy App
    """

    _endpoint: ClassVar[str] = "/api/orderSharing"

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
    def get_budget(cls, **metadata) -> "OrderSharing":
        endpoint = f"{cls._endpoint}/newOrder/json/web"
        resp = cls._client.put(endpoint, json=dict(metadata=metadata))
        return cls(**resp)
