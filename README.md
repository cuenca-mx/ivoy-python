# iVoy

[![test](https://github.com/cuenca-mx/ivoy-python/workflows/test/badge.svg)](https://github.com/cuenca-mx/ivoy-python/actions?query=workflow%3Atest)
[![codecov](https://codecov.io/gh/cuenca-mx/ivoy-python/branch/master/graph/badge.svg)](https://codecov.io/gh/cuenca-mx/ivoy-python)

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