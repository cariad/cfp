from dataclasses import dataclass
from typing import TypeVar, Union


@dataclass
class Source:
    pass


AnySource = Union[str, Source]

# TSource = TypeVar("TSource", bound=Source)
# TSource = TypeVar("TSource", str, Source)
TSource = TypeVar("TSource", bound=AnySource)
