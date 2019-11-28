from typing import ClassVar


class Resource:
    _client: ClassVar['ivoy.Client']  # type: ignore
    _endpoint: ClassVar[str]
