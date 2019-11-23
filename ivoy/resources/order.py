import copy
import datetime as dt
from dataclasses import dataclass, field
from typing import ClassVar, List, Optional, Union

from .base import Resource


@dataclass
class Order(Resource):
    """
    Based on: http://docs.ivoy.mx/express/#órdenes
    """

    _endpoint: ClassVar[str] = "/api/order"

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
    ivoy_json_default = {
        "data": {
            "bOrder": {
                "device": "api",
                "orderType": {
                    "idOrderType": 1
                },
                "packageType": {
                    "idPackageType": 1
                },
                "paymentMethod": {
                    "idPaymentMethod": 4
                },
                "orderAddresses": [
                    {
                        "isPickup": 1,
                        "isSource": 1,
                        "address": {}
                    }
                ]
            }
        }
    }

    @classmethod
    def create(cls, **metadata) -> "Order":
        endpoint = f"{cls._endpoint}/newOrder/json/web"
        json_data = self._create_json()
        resp = cls._client.put(endpoint, json=json_data)
        return cls(**resp)

    @classmethod
    def retrieve(cls, identity_id: str) -> "Order":
        endpoint = f"{cls._endpoint}/getById/json/web"
        json_data = self._update_json(identity_id)
        resp = cls._client.post(endpoint, json=json_data)
        return cls(**resp)

    @classmethod
    def cancel(cls, identity_id: str) -> "Order":
        endpoint = f"{cls._endpoint}/cancelOrder/json/web"
        json_data = self._update_json(identity_id)
        resp = cls._client.put(endpoint, json=json_data)
        return cls(**resp)

    @staticmethod
    def _create_json(self, customer_orders: list) -> dict:
        json_data = copy.deepcopy(ivoy_json_default)
        json_data = self._card_collection_address(json_data)
        json_data = self._logged_agent(json_data)
        json_data = self._order_addresses(json_data)
        return json_data

    @staticmethod
    def _update_json(identity_id: str) -> dict:
        json_data = {
            "data": {
                "bOrder": {
                    "idOrder": identity_id
                }
            }
        }
        return json_data

    @staticmethod
    def _card_collection_address(self, json_data: dict) -> dict:
        card_collection_address = config.get_value(
            "CARD_COLLECTION_ADDRESS"
        )
        item = json_data['data']['bOrder']['orderAddresses'][0]
        item['address'] = dict(
            latitude=card_collection_address['latitude'],
            longitude=card_collection_address['longitude'],
            neighborhood=card_collection_address['neighborhood'],
            street=card_collection_address['street'],
            zipCode=card_collection_address['zipCode'],
            externalNumber=card_collection_address['externalNumber'],
        )
        item['comment'] = card_collection_address['comment']
        return json_data

    @staticmethod
    def _logged_agent(self, json_data: dict) -> dict:
        email = get_jwt_identity()
        agents = config.get_value("AGENTS")
        emails = [agent['email'] for agent in agents]
        if email not in emails:
            email = "soporte@cuenca.com"
        for agent in agents:
            if agent['email'] == email:
                item = json_data['data']['bOrder']['orderAddresses'][0]
                item['personApproved'] = agent['name']
                item['phone'] = agent['phone']
                break
        return json_data

    @staticmethod
    def _order_addresses(
        json_data: dict,
        customer_orders: list
    ) -> dict:
        for customer_order in customer_orders:
            latitud, longitud = get_location(customer_order)
            geocoding_gmaps = customer_order['geocoding_gmaps']
            comment = ""
            if 'folio' in customer_order:
                comment = f"""
                    Entregar folio: {customer_order['folio']} |
                    Comentario del cliente:
                    {geocoding_gmaps.get('comment', 'N/A')}
                """
            json_data["data"]['bOrder']['orderAddresses'].append({
                "isPickup": 0,
                "isSource": 0,
                'comment': comment,
                "personApproved": customer_order['client_name'],
                "phone": customer_order['telephone'].replace("+521", ""),
                "address": {
                    'externalNumber': get_type_for_ivoy(
                        geocoding_gmaps, ['street_number']
                    ),
                    'internalNumber': geocoding_gmaps.get('internal_number',
                                                          ''),
                    "latitude": str(latitud),
                    "longitude": str(longitud),
                    'neighborhood': get_type_for_ivoy(geocoding_gmaps, [
                        "political",
                        "sublocality",
                        "sublocality_level_1"
                    ]),
                    'street': get_type_for_ivoy(geocoding_gmaps, 
                                                ['route']),
                    'zipCode': get_type_for_ivoy(geocoding_gmaps,
                                                 ['postal_code']),
                }
            })
        return json_data

