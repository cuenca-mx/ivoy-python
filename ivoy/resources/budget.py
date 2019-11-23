import datetime as dt
from dataclasses import dataclass, field
from typing import ClassVar, List, Optional, Union

from ..types import OrderAddress
from .base import Resource


@dataclass
class Budget(Resource):
    """
    Based on: http://docs.ivoy.mx/express/#cotización
    """

    _endpoint: ClassVar[str] = "/api/validZipCode/json/web"

    @classmethod
    def create(
        cls, 
        origin: OrderAddress, 
        destiny: OrderAddress, 
        **metadata
    ) -> "Budget":
        body = dict(
            data= dict(
                bOrder = dict(
                    orderAddresses = list(
                        origin.to_dict(),
                        destiny.to_dict()
                    )
                )
            )
        )
        resp = cls._client.put(self._endpoint, json=body)
        return cls(**resp)