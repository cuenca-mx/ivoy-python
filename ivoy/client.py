from typing import Any, ClassVar, Dict, Optional, Tuple

from requests import Response, Session

from resources import Authentication, Budget, Order, OrderSharing, Resource

API_URL = "https://api.ivoy.dev"


class Client:

    base_url: ClassVar[str] = API_URL
    user_credentials: Tuple[Optional[str], Optional[str]]  # user, password
    token: Optional[str]
    headers: Dict[str, str]
    session: Session

    # resources
    authentication: ClassVar = Authentication
    budget: ClassVar = Budget
    order: ClassVar = Order
    order_sharing: ClassVar = OrderSharing

    def __init__(
        self,
        user: Optional[str] = None,
        password: Optional[str] = None,
        token: Optional[str] = None,
    ):
        self.session = Session()
        self.headers = {"Content-Type": "application/json"}
        self.user_credentials = (user, password)
        self.token = token
        Resource._client = self

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
