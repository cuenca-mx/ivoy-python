import os
from typing import Any, ClassVar, Dict, Optional

from requests import Response, Session

from .exc import ExpiredTokens, raise_ivoy_exception
from .resources import (
    Budget,
    CarrierLocation,
    Order,
    OrderSharing,
    Package,
    Waybill,
)

API_URL = os.environ['IVOY_URL']
WEB_URL = os.environ['IVOY_WEB_URL']


class Client:
    base_url: ClassVar[str] = API_URL
    web_url: ClassVar[str] = WEB_URL
    auth_user: str
    auth_password: str
    web_auth_user: str
    web_auth_password: str
    same_day_auth_user: str
    same_day_auth_password: str
    ivoy_user: str
    ivoy_password: str
    token: Optional[str]
    web_token: Optional[str]
    same_day_token: Optional[str]
    id_client: Optional[str]
    session: Session

    # resources
    @property
    def order(self):
        Order._client = self
        return Order

    @property
    def package(self):
        Package._client = self
        return Package

    @property
    def budget(self):
        Budget._client = self
        return Budget

    @property
    def carrier_location(self):
        CarrierLocation._client = self
        return CarrierLocation

    @property
    def order_sharing(self):
        OrderSharing._client = self
        return OrderSharing

    @property
    def waybill(self):
        Waybill._client = self
        return Waybill

    def __init__(
        self,
        auth_user: Optional[str] = None,
        auth_password: Optional[str] = None,
        ivoy_user: Optional[str] = None,
        ivoy_password: Optional[str] = None,
        web_auth_user: Optional[str] = None,
        web_auth_password: Optional[str] = None,
        same_day_auth_user: Optional[str] = None,
        same_day_auth_password: Optional[str] = None,
    ):
        self.session = Session()
        self.auth_user = auth_user or os.environ['IVOY_AUTH_USER']
        self.auth_password = auth_password or os.environ['IVOY_AUTH_PASS']
        self.web_auth_user = web_auth_user or os.environ['IVOY_WEB_AUTH_USER']
        self.web_auth_password = (
            web_auth_password or os.environ['IVOY_WEB_AUTH_PASS']
        )
        self.same_day_auth_user = (
            same_day_auth_user or os.environ['IVOY_SAME_DAY_AUTH_USER']
        )
        self.same_day_auth_password = (
            same_day_auth_password or os.environ['IVOY_SAME_DAY_AUTH_PASS']
        )
        self.ivoy_user = ivoy_user or os.environ['IVOY_USER']
        self.ivoy_password = ivoy_password or os.environ['IVOY_PASS']
        self.token = None
        self.web_token = None
        self.same_day_token = None
        self.id_client = os.environ['IVOY_ID_CLIENT'] or None

    def get_token(
        self, web_token: bool = False, same_day_token: bool = False
    ) -> str:
        url = f'{self.base_url}/api/login/loginClient/json/web'
        if web_token:
            auth = (self.web_auth_user, self.web_auth_password)
        elif same_day_token:
            auth = (self.same_day_auth_user, self.same_day_auth_password)
        else:
            auth = (self.auth_user, self.auth_password)
        json_data = dict(
            data=dict(
                systemRequest=dict(
                    user=self.ivoy_user, password=self.ivoy_password,
                ),
            ),
        )
        response = self.session.request('POST', url, auth=auth, json=json_data)
        self._check_response(response)
        data = response.json()
        self.id_client = data['data']['idClient']
        return data['token']['access_token']

    def post(self, endpoint: str, **kwargs: Any) -> Response:
        return self.request('post', endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs: Any) -> Response:
        return self.request('put', endpoint, **kwargs)

    def request(self, method: str, endpoint: str, **kwargs: Any,) -> Response:
        if 'orderSharing' in endpoint:
            url = self.web_url + endpoint
        else:
            url = self.base_url + endpoint
        is_waybill = 'getMassiveTags' in endpoint
        self.init_tokens()
        if 'Package' in endpoint or 'MassiveTags' in endpoint:
            headers = self.create_headers(endpoint, same_day=True)
        else:
            headers = self.create_headers(endpoint)
        response = self.session.request(
            method, url, headers=headers, timeout=90, **kwargs
        )
        try:
            self._check_response(response, is_waybill)
        except ExpiredTokens:
            # Try to generate Tokens again and retry request
            self.init_tokens(force=True)
            headers = self.create_headers(endpoint)
            response = self.session.request(
                method, url, headers=headers, **kwargs
            )
            self._check_response(response, is_waybill)
        return response

    def init_tokens(self, force: bool = False) -> None:
        if not self.token or force:
            self.token = self.get_token()
        if not self.web_token or force:
            self.web_token = self.get_token(web_token=True)
        if not self.same_day_token or force:
            self.same_day_token = self.get_token(same_day_token=True)

    def create_headers(
        self, endpoint: str, same_day: bool = False
    ) -> Dict[str, Any]:
        if 'orderSharing' in endpoint:
            return {
                'Content-type': 'application/json',
                'Token': self.web_token,
            }
        else:
            if same_day:
                return {
                    'Content-type': 'application/json',
                    'Token': self.same_day_token,
                }
            else:
                return {
                    'Content-type': 'application/json',
                    'Token': self.token,
                }

    @staticmethod
    def _check_response(response: Response, is_waybill: bool = False) -> None:
        if response.ok:
            if is_waybill:
                return
            json = response.json()
            if 'code' in json and json['code'] == 0:
                return
            elif 'code' in json and json['code'] == -156:
                # Tokens expired. Based on http://docs.ivoy.mx/express/#errores
                # All error codes come from API as negative numbers.
                raise ExpiredTokens(156, 'Tokens have expired.')
            else:
                raise_ivoy_exception(json['code'], json['message'])
        response.raise_for_status()
