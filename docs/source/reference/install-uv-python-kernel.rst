Install uv and create a Python kernel
=====================================

Use this recipe on the HPC when you want a Python notebook kernel managed by
``uv``. It starts with installing ``uv`` and ends with a named Jupyter kernel
that VS Code or Cursor can select through the remote Jupyter server.

Install uv
----------

Use the official standalone installer from Astral:

.. code-block:: console

   $ curl -LsSf https://astral.sh/uv/install.sh | sh

If ``curl`` is not available, use ``wget``:

.. code-block:: console

   $ wget -qO- https://astral.sh/uv/install.sh | sh

Restart the shell, source the profile file updated by the installer, or add the
reported install directory to ``PATH``. Then confirm ``uv`` is available:

.. code-block:: console

   $ uv --version

See the official `uv installation guide <https://docs.astral.sh/uv/getting-started/installation/>`__
for platform-specific options, version pinning, upgrades, and installer
configuration.

Create or enter the project
---------------------------

Move to the HPC project directory that will provide the Python environment:

.. code-block:: console

   $ cd <project-dir>

If the project is not already managed by ``uv``, initialize it or make sure it
has a valid ``pyproject.toml``:

.. code-block:: console

   $ uv init

Add the Jupyter kernel dependency and any project packages:

.. code-block:: console

   $ uv add --dev ipykernel
   $ uv add pandas matplotlib

Register the kernel
-------------------

Register the uv environment as a named Jupyter kernel:

.. code-block:: console

   $ uv run ipython kernel install \
       --user \
       --name py-ai-bunker \
       --display-name "Python (ai-bunker)"

The ``--name`` value is the internal kernel identifier. The ``--display-name``
value is what users see in the notebook kernel picker.

Verify the kernel
-----------------

List available kernels from the HPC:

.. code-block:: console

   $ jupyter kernelspec list

Start or refresh the remote Jupyter server, then select ``Python (ai-bunker)``
from VS Code or Cursor.
