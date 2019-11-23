import datetime as dt
import os

from typing import Any, ClassVar, Dict, Optional, Tuple
from requests import Response, Session

from .resources import Budget, Order, OrderSharing, Resource

API_URL = "https://api.ivoy.dev"


class Client:

	base_url: ClassVar[str] = API_URL
	auth_user: str
	auth_password: str
	sys_user: str
	sys_password: str
	token: Optional[str]
	headers: Dict[str, str]
	session: Session
	token_expires_at: dt.datetime # token expire date

	# resources
	budget: ClassVar = Budget
	order: ClassVar = Order
	order_sharing: ClassVar = OrderSharing

	def __init__(
		self,
		auth_user: str,
		auth_password: str,
		ivoy_user: str,
		ivoy_password: str,
	):
		self.session = Session()
		self.auth_user = auth_user
		self.auth_password = auth_password
		self.ivoy_user = ivoy_user
		self.ivoy_password = ivoy_password
		self.token, self.token_expires_at = self.get_token()
		self.headers = {
			'Content-type': 'application/json',
			'Token': self.token
		}
		Resource._client = self


	def check_token(self) -> None:
		now = dt.datetime.utcnow()
		if now > self.token_expires_at:
			self.token, self.token_expires_at = self.get_token()


	def get_token(self) -> Tuple[str, str]:
		url = f'{self.base_url}/api/login/loginClient/json/web'
		response = self.session.request(
			'POST',
			url,
			auth=(self.auth_user, self.auth_password),
			json={
				'data': {
					'systemRequest': {
						'user': self.ivoy_user,
						'password': self.ivoy_password
					}
				}
			}
		)
		data = response.json()
		expires_at = dt.datetime.strptime(data['token']['expires_in'], 
										  '%d/%m/%y %H:%M')
		return data['token']['access_token'], expires_at


	def post(self, endpoint: str, **kwargs: Any) -> Dict[str, Any]:
		return self.request("post", endpoint, **kwargs)

	def put(self, endpoint: str, **kwargs: Any) -> Dict[str, Any]:
		return self.request("put", endpoint, **kwargs)

	def request(
		self,
		method: str,
		endpoint: str,
		token_score: Optional[str] = None,
		**kwargs: Any,
	) -> Dict[str, Any]:
		self.check_token()
		url = self.base_url + endpoint
		headers = {**self.headers}
		response = self.session.request(method, url, headers=headers, **kwargs)
		self._check_response(response)
		return response.json()

	@staticmethod
	def _check_response(response: Response) -> None:
		if response.ok:
			return
		response.raise_for_status()
