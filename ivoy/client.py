import os
from typing import Any, ClassVar, Dict, Optional

from requests import Response, Session

from .exc import ExpiredTokens, IvoyException
from .resources import Budget, Order, OrderSharing, Resource

API_URL = os.environ['IVOY_URL']
WEB_URL = os.environ['IVOY_WEB_URL']


class Client:

    base_url: ClassVar[str] = API_URL
    web_url: ClassVar[str] = WEB_URL
    auth_user: str
    auth_password: str
    web_auth_user: str
    web_auth_password: str
    ivoy_user: str
    ivoy_password: str
    token: Optional[str]
    web_token: Optional[str]
    session: Session

    # resources
    budget: ClassVar = Budget
    order: ClassVar = Order
    order_sharing: ClassVar = OrderSharing

    def __init__(
        self,
        auth_user: Optional[str] = None,
        auth_password: Optional[str] = None,
        ivoy_user: Optional[str] = None,
        ivoy_password: Optional[str] = None,
        web_auth_user: Optional[str] = None,
        web_auth_password: Optional[str] = None,
    ):
        self.session = Session()
        self.auth_user = auth_user or os.environ['AUTH_USER']
        self.auth_password = auth_password or os.environ['AUTH_PASS']
        self.web_auth_user = web_auth_user or os.environ['WEB_AUTH_USER']
        self.web_auth_password = (
            web_auth_password or os.environ['WEB_AUTH_PASS']
        )
        self.ivoy_user = ivoy_user or os.environ['IVOY_USER']
        self.ivoy_password = ivoy_password or os.environ['IVOY_PASS']
        self.token = self.get_token()
        self.web_token = self.get_token(True)
        Resource._client = self

    def get_token(self, web_token: bool = False) -> str:
        url = f'{self.base_url}/api/login/loginClient/json/web'
        if web_token:
            auth = (self.web_auth_user, self.web_auth_password)
        else:
            auth = (self.auth_user, self.auth_password)
        response = self.session.request(
            'POST',
            url,
            auth=auth,
            json={
                'data': {
                    'systemRequest': {
                        'user': self.ivoy_user,
                        'password': self.ivoy_password,
                    }
                }
            },
        )
        self._check_response(response)
        data = response.json()
        return data['token']['access_token']

    def post(self, endpoint: str, **kwargs: Any) -> Dict[str, Any]:
        return self.request('post', endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs: Any) -> Dict[str, Any]:
        return self.request('put', endpoint, **kwargs)

    def request(
        self, method: str, endpoint: str, **kwargs: Any,
    ) -> Dict[str, Any]:
        if 'orderSharing' in endpoint:
            url = self.web_url + endpoint
        else:
            url = self.base_url + endpoint
        headers = self.create_headers(endpoint)
        response = self.session.request(method, url, headers=headers, **kwargs)

        try:
            self._check_response(response)
        except ExpiredTokens:
            # Try to generate Tokens again and retry request
            self.token = self.get_token()
            self.web_token = self.get_token(True)
            headers = self.create_headers(endpoint)
            response = self.session.request(
                method, url, headers=headers, **kwargs
            )
            self._check_response(response)
        except IvoyException as ivoyexc:
            raise IvoyException(ivoyexc.code, ivoyexc.message)
        except Exception as e:
            raise Exception(e)

        return response.json()

    def create_headers(self, endpoint: str) -> Dict[str, Any]:
        if 'orderSharing' in endpoint:
            return {
                'Content-type': 'application/json',
                'Token': self.web_token,
            }
        else:
            return {
                'Content-type': 'application/json',
                'Token': self.token,
            }

    @staticmethod
    def _check_response(response: Response) -> None:
        if response.ok:
            json = response.json()
            if 'code' in json and json['code'] == 0:
                return
            elif 'code' in json and json['code'] == -156:
                # Tokens expired. Based on http://docs.ivoy.mx/express/#errores
                # All error codes come from API as negative numbers.
                raise ExpiredTokens(156, 'Tokens have expired.')
            else:
                raise IvoyException(
                    json['code'], 'iVoy API error: {}'.format(json['message'])
                )
        response.raise_for_status()
