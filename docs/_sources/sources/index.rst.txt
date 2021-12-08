Sources
=======

**CFP** can set parameters to any value that has a supported *source*.

This module describes all the baked-in sources.

- To read a value from Systems Manager Parameter Store, pass :py:class:`cfp.sources.FromParameterStore`.
- To use the parameter's previous value, pass :py:class:`cfp.sources.UsePreviousValue`.

.. toctree::

   from-parameter-store
   use-previous
