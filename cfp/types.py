from typing import TypedDict

StackParameterKey = str
RegionName = str


class ApiParameter(TypedDict, total=False):
    ParameterKey: StackParameterKey
    ParameterValue: str
    UsePreviousValue: bool
