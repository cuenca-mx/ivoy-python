# iVoy

[![Build Status](https://travis-ci.com/cuenca-mx/ivoy-python.svg?token=KUPW5wq7zSydeEVhVfVe&branch=master)](https://travis-ci.com/cuenca-mx/ivoy-python)
[![Coverage Status](https://coveralls.io/repos/github/cuenca-mx/ivoy-python/badge.svg?branch=master&t=VaY2TA)](https://coveralls.io/github/cuenca-mx/ivoy-python?branch=master)

[iVoy Mensajería](https://ivoy.mx) Python3.6+ Client Library

## Install

To setup your environment:

```bash
pip install ivoy
```

## Tests

```bash
make test
```

## Create Client

```python
from ivoy import Client

client = Client(
	auth_user= your_auht_user,
	auth_password= your_auth_password,
	ivoy_user= ivoy_system_user,
	ivoy_password= ivoy_system_password
)
```