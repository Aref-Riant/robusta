Customizing Playbooks
##############################

Robusta is a powerful rules engine for devops, but it needs rules to tell it what to do. These rules are called "playbooks".

Enabling a new playbook
------------------------

1. Enable the ``deployment_babysitter`` playbook:

.. admonition:: values.yaml

    .. code-block:: yaml

       playbooks:
         - name: "deployment_babysitter"
           action_params:
             fields_to_monitor: ["spec.replicas"]


This playbook monitors changes to deployments. You can see all the settings in the :ref:`playbook's documentation <deployment_babysitter>`.

2. Perform an upgrade with Helm to apply the new configuration

Seeing your new config in action
----------------------------------

1. Scale one of your deployments:

.. code-block:: python

   kubectl scale --replicas NEW_REPLICAS_COUNT deployments/DEPLOYMENT_NAME


2. Check the slack channel you configured when installing Robusta:

.. admonition:: Example Slack Message

    .. image:: ../images/replicas_change.png

How it works
----------------------------------
In the playbooks configuration, we asked to get notified every time the ``'spec.replicas'`` field changes.

Scaling the deployment triggered a notification.

Try changing the configuration in ``values.yaml`` so that Robusta monitors changes to a deployment's image tag too.
