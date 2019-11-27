import pytest

from ivoy import Client
from ivoy.resources import OrderSharing

@pytest.mark.vcr
def test_order_sharing():
    client = Client(
    	auth_user= 'auth_user',
	    auth_password= 'auth_password',
	    web_auth_user= 'web_auth_user',
	    web_auth_password= 'web_auth_password',
	    ivoy_user= 'ivoy_user',
	    ivoy_password= 'ivoy_password'
	)
    order_sharing = client.order_sharing.get_tracking_url(1437397)
    assert order_sharing
    assert type(order_sharing) == OrderSharing
    assert order_sharing.id == 1437397
    assert order_sharing.tracking_url == 'https://v2.ivoy.mx/client/app/share/ABCDEG='

