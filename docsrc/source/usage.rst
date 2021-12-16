Usage
=====

In a nutshell
-------------

1. Create an instance of :py:class:`cfp.StackParameters`.
2. Call :py:func:`cfp.StackParameters.add` to set the parameter values.
3. Pass :py:attr:`cfp.StackParameters.api_parameters` to your Boto3 function.

Setting parameter values
------------------------

Known values
~~~~~~~~~~~~

To pass known (hard-coded or otherwise looked-up) values, simply call :py:func:`cfp.StackParameters.add` with those values.

For example:

.. code-block:: python

   from cfp import StackParameters

   sp = StackParameters()
   sp.add("ParameterA", "Value A")
   sp.add("ParameterB", "Value B")

Previous values
~~~~~~~~~~~~~~~

To use a parameter's previous value, pass an instance of :class:`cfp.sources.UsePreviousValue`.

For example:

.. code-block:: python

   from cfp import StackParameters
   from cfp.sources import UsePreviousValue

   sp = StackParameters()
   sp.add("InstanceType", UsePreviousValue())


Systems Manager Parameter Store look-ups
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To look-up and set values from Systems Manager Parameter Store, set the parameter's value to an instance of :class:`cfp.sources.FromParameterStore`.

While CloudFormation does have baked-in support for reading Systems Manager parameters, it can read only parameters in the same region and account as your stack. CFP supports cross-region and cross-account look-ups.

The following example reads three parameters:

1. ``/instance-type`` is read using the current default credentials and region.
2. ``/log-level`` is read using the current default credentials from "eu-west-2".
3. ``/secret-sauce`` is read using a Boto3 session crafted for reading from a different AWS account.

.. code-block:: python

   from cfp import StackParameters
   from cfp.sources import FromParameterStore

   sp = StackParameters()

   sp.add(
      "InstanceType",
      FromParameterStore("/instance-type"),
   )

   sp.add(
      "LogLevel",
      FromParameterStore("/log-level", region="eu-west-2"),
   )

   sp.add(
      "SecretSauce",
      FromParameterStore("/secret-sauce", session=other_account),
   )

Passing stack parameters to Boto3
---------------------------------

The :py:attr:`cfp.StackParameters.api_parameters` property can be passed directly to Boto3 functions like the CloudFormation client's ``create_change_set()``.

For example:

.. code-block:: python

   from cfp import StackParameters
   from boto3.session import Session

   sp = StackParameters()
   sp.add("ParameterA", "Value A")
   sp.add("ParameterB", "Value B")

   client = session.client("cloudformation")
   client.create_change_set(
      StackName="MyStack",
      ChangeSetName="MyChangeSet",
      ChangeSetType="UPDATE",
      Parameters=sp.api_parameters,
      TemplateBody="...",
   )

Logging parameter values
------------------------

The :py:func:`cfp.StackParameters.render` function renders the full set of parameters and their values to a string writer.

For example:

.. testcode::

   from cfp import StackParameters
   from io import StringIO


   sp = StackParameters()
   sp.add("ParameterA", "Value A")
   sp.add("ParameterB", "Value B")

   writer = StringIO()
   sp.render(writer, color=False)

   print(writer.getvalue())

.. testoutput::
   :options: +NORMALIZE_WHITESPACE

   ParameterA = Value A
   ParameterB = Value B

Unit testing
------------

Say you have a function that builds and returns :class:`cfp.StackParameters`:

.. code-block:: python

   from cfp import StackParameters
   from cfp.sources import FromParameterStore

   def parameters() -> StackParameters:
      sp = StackParameters()
      sp.add("ParameterA", "Value A")
      sp.add("ParameterB", FromParameterStore("/b"))
      return sp

You can unit test this function by asserting on the length of the :class:`cfp.StackParameters` as well as the sources of each parameter key:

.. code-block:: python

   from cfp import StackParameters
   from cfp.sources import FromParameterStore
   from example import parameters

   def test_parameters__len() -> None:
      sp = parameters()
      assert len(sp) == 2

   def test_parameters__param_a() -> None:
      sp = parameters()
      assert sp["ParameterA"] == "Value A"

   def test_parameters__param_b() -> None:
      sp = parameters()
      assert sp["ParameterB"] == FromParameterStore("/b")
