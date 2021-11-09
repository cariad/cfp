Examples
========

Hard-coded values
-----------------

To construct a parameter set with hard-coded values, call :meth:`.add` with the keys and values:

.. testcode::

   from cfp import StackParameters

   sp = StackParameters()
   sp.add("ParameterA", "Value A")
   sp.add("ParameterB", "Value B")

   print(sp.api_parameters)

.. testoutput::

   [{'ParameterKey': 'ParameterA', 'ParameterValue': 'Value A'}, {'ParameterKey': 'ParameterB', 'ParameterValue': 'Value B'}]

The :py:attr:`.api_parameters` property can be passed directly to boto3:

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
      ChangeSetType="UPDATE,
      Parameters=sp.api_parameters,
      TemplateBody="...",
   )

Parameter Store look-up
-----------------------

To look-up a value in Systems Manager Parameter Store, set the parameter's value to a :class:`.FromParameterStore` instance:

.. testcode::

   from cfp import FromParameterStore, StackParameters

   sp = StackParameters()
   sp.add("ParameterA", FromParameterStore("/cfp/example1"))
   sp.add("ParameterB", FromParameterStore("/cfp/example2"))

   print(sp.api_parameters)

.. testoutput::

   [{'ParameterKey': 'ParameterA', 'ParameterValue': 'foo'}, {'ParameterKey': 'ParameterB', 'ParameterValue': 'bar'}]
