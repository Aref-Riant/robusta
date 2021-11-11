Manual Triggers
##############################

All the playbooks we have seen so far respond to events in your cluster.
You can also run playbooks on demand.

In this example we'll manually trigger a playbook which profiles a Python application in your cluster. No prior setup for the Python application is necessary!

Deploy an example Python application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
First we need a Python application to profile.

Enable the python_profiler playbook
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The :ref:`python_profiler` playbook is enabled by default. If you changed the default configuration, make sure you have the following in your values.yaml

.. code-block:: bash

    playbooks:
      - name: "python_profiler"

Manually triggering the python_profiler playbook
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    robusta playbooks trigger python_profiler pod_name=<POD_NAME> namespace=<NAMESPACE>
