from typing import ClassVar

import ivoy


class Resource:
    _client: ClassVar['ivoy.Client']  # type: ignore
    _endpoint: ClassVar[str]
