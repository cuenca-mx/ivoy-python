import json

import pytest
from vcr.request import Request  # type: ignore


@pytest.fixture(scope='module')
def vcr_config() -> dict:
    config = dict()
    config['filter_headers'] = [('Authorization', None), ('Token', None)]
    config['before_record_request'] = scrub_body_request  # type: ignore
    config['before_record_response'] = scrub_body_response  # type: ignore
    config['decode_compressed_response'] = True  # type: ignore
    return config


def scrub_body_request(request: Request) -> dict:
    body = request.body.decode('utf-8')
    body_dict = json.loads(body)
    try:
        body_dict['data']['systemRequest']['user'] = 'USER'
        body_dict['data']['systemRequest']['password'] = 'PASS'
    except KeyError:
        pass

    request.body = json.dumps(body_dict)
    return request


def scrub_body_response(response: dict) -> dict:
    if type(response['body']['string']) != bytes:
        if (
            'token' in response['body']['string'].decode()
            and 'isActive' in response['body']['string'].decode()
        ):
            response['body']['string'] = json.dumps(
                dict(
                    code=0,
                    token=dict(access_token='123'),
                    data=dict(idClient=69319),
                )
            ).encode('utf-8')
    return response
