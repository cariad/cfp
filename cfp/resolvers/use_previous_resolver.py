from typing import Iterator, List

from cfp.resolvers.resolver import Resolver
from cfp.sources import UsePreviousValue
from cfp.types import ApiParameter, StackParameterKey


class UsePreviousValueResolver(Resolver[UsePreviousValue]):
    def __init__(self) -> None:
        self._keys: List[StackParameterKey] = []

    def _queue(self, key: StackParameterKey, source: UsePreviousValue) -> None:
        self._keys.append(key)

    def resolve(self) -> Iterator[ApiParameter]:
        """
        Invokes the queued resolution tasks and returns an iterator of the
        values.
        """

        for key in self._keys:
            yield ApiParameter(
                ParameterKey=key,
                UsePreviousValue=True,
            )
