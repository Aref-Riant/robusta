Customizing built-in playbooks
##############################

Robusta is a powerful rules engine for devops, but it needs rules to tell it what to do. These rules are called "playbooks".

Enabling a new playbook
------------------------

Lets edit ``active_playbooks.yaml`` and add the following:

.. code-block:: yaml

   (...)
   active_playbooks:
     (...)
     - name: "deployment_babysitter"
       action_params:
         fields_to_monitor: ["spec.replicas"]


This will add an additional playbook named ``deployment_babysitter`` - a playbook that monitors changes to deployments.

How did we know which parameters we could use with the ``deployment_babysitter`` playbook? It's simple. We read it's documentation in the :ref:`list of builtin playbooks <deployment_babysitter>`.

Deploy your new config
------------------------
So far we have edited the configuration file locally. Lets deploy it to Robusta inside your Kubernetes cluster.

From the playbooks directory run:

.. code-block:: python

   robusta playbooks configure active_playbooks.yaml


Alternatively, you can create a new Helm release using your updated ``active_playbooks.yaml`` file.

Seeing your new config in action
----------------------------------
Scale one of your deployments using the command below:

.. code-block:: python

   kubectl scale --replicas NEW_REPLICAS_COUNT deployments/DEPLOYMENT_NAME

Now, open the slack channel you configured when installing Robusta. A deployment change notification should appear:

.. image:: ../images/replicas_change.png

How it works
----------------------------------
In the playbooks configuration, we asked to get notified every time the ``'spec.replicas'`` field changes.

Scaling the deployment triggered a notification.

Try changing the configuration in ``active_playbooks.yaml`` so that Robusta monitors changes to a deployment's image tag too.
