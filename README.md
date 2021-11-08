# cfp

[![CircleCI](https://circleci.com/gh/cariad/cfp/tree/main.svg?style=shield)](https://circleci.com/gh/cariad/cfp/tree/main) [![codecov](https://codecov.io/gh/cariad/cfp/branch/main/graph/badge.svg?token=xyqHGoOyMM)](https://codecov.io/gh/cariad/cfp)

**cfp** is a Python package for building Amazon Web Services **C**loud**F**ormation stack **p**arameters.

In particular, cfp helps to efficiently reference parameter values in Parameter Store, even across accounts and regions.

The output is compatible with boto3.

## Examples

```python
from cfp import StackParameters

sp = StackParameters()
sp.add("ParameterA", "Value A")
sp.add("ParameterB", "Value B")

print(sp.api)
```

```python
[{'ParameterKey': 'ParameterA', 'ParameterValue': 'Value A'}, {'ParameterKey': 'ParameterB', 'ParameterValue': 'Value B'}]
```

```python
from cfp import StackParameters
from boto3.session import Session

sp = StackParameters()
sp.add("ParameterA", "Value A")
sp.add("ParameterB", "Value B")

client = session.client("cloudformation")
client.create_change_set(
    StackName="MyStack",
    ChangeSetName="MyChangeSet",
    ChangeSetType="UPDATE,
    Parameters=sp.api,
    TemplateBody="...",
)
```

To look-up a value in Systems Manager Parameter Store, set the parameter's value to a `.FromParameterStore` instance:

```python
from cfp import FromParameterStore, StackParameters

sp = StackParameters()
sp.add("ParameterA", FromParameterStore("/cfp/example1"))
sp.add("ParameterB", FromParameterStore("/cfp/example2"))

print(sp.api)
```

```python
[{'ParameterKey': 'ParameterA', 'ParameterValue': 'foo'}, {'ParameterKey': 'ParameterB', 'ParameterValue': 'bar'}]
```

Read the full documentation at [cariad.github.io/cfp](https://cariad.github.io/cfp).

## 👋 Hello!

**Hello!** I'm [Cariad Eccleston](https://cariad.io) and I'm an independent/freelance software engineer. If my work has value to you, please consider [sponsoring](https://github.com/sponsors/cariad/).

If you ever raise a bug, request a feature or ask a question then mention that you're a sponsor and I'll respond as a priority. Thank you!
