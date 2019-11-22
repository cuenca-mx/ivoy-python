from typing import ClassVar, Optional


class Resource:
    _client: ClassVar["ivoy.Client"]  # type: ignore
    _endpoint: ClassVar[str]
    _token_score: ClassVar[Optional[str]] = None
