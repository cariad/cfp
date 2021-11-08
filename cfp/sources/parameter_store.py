from dataclasses import dataclass
from typing import Optional

from boto3.session import Session

from cfp.sources.source import Source


@dataclass
class FromParameterStore(Source):
    name: str
    region: Optional[str] = None
    session: Optional[Session] = None
