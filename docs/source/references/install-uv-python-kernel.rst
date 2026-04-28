Install uv and create a Python kernel
=====================================

Use this recipe on the HPC when you want a Python notebook kernel managed by
``uv``. It starts with installing ``uv`` and ends with a named Jupyter kernel
that VS Code or Cursor can select through the remote Jupyter server.

``uv`` is a fast Python package and project manager from Astral. It is a good
fit when your analysis code is a Python project with a ``pyproject.toml`` file,
when you want dependencies recorded with the project, or when you want the same
environment to work for notebooks, scripts, tests, and command-line tools. In
this workflow, ``uv`` creates the Python environment on the HPC and registers it
as a Jupyter kernel.

Install uv
----------

Use the official standalone installer from Astral:

.. tabs::

   .. tab:: curl

      .. code-block:: console

         $ curl -LsSf https://astral.sh/uv/install.sh | sh

   .. tab:: wget

      .. code-block:: console

         $ wget -qO- https://astral.sh/uv/install.sh | sh

After the installer finishes, the ``uv`` executable may not be visible in the
current shell yet. The installer usually prints the directory where it placed
``uv`` and may also update a shell startup file such as ``~/.bashrc``,
``~/.bash_profile``, or ``~/.zshrc``.

Use one of these options before continuing:

* Start a new login shell by logging out and back in to the HPC, or by opening
  a new terminal session.
* Reload the updated shell profile in the current session, for example:

  .. code-block:: console

     $ source ~/.bashrc

  If your site uses another shell, source the startup file for that shell
  instead.
* If the installer printed a directory that contains the ``uv`` binary, add it
  to ``PATH`` for the current session before testing the command.

Then confirm that ``uv`` is available:

.. code-block:: console

   $ uv --version

See the official `uv installation guide <https://docs.astral.sh/uv/getting-started/installation/>`__
for platform-specific options, version pinning, upgrades, and installer
configuration.

Create a project from scratch
-----------------------------

The ``pyproject.toml`` file is the project recipe for the Python environment.
It records the packages needed by the notebook code, while ``uv.lock`` records
the exact resolved package versions. Together, those files let another HPC
session recreate the same environment with ``uv sync``.

Create a new HPC project directory if you do not already have one:

.. code-block:: console

   $ mkdir -p <project-dir>
   $ cd <project-dir>

Initialize the project:

.. code-block:: console

   $ uv init

This creates a starter ``pyproject.toml``. Add the Jupyter kernel dependency and
any project packages:

.. code-block:: console

   $ uv add --dev ipykernel
   $ uv add pandas matplotlib

After these commands, ``pyproject.toml`` contains the declared dependencies and
``uv.lock`` contains the locked versions. Commit both files if this project is
safe to version-control.

Use an existing pyproject.toml
------------------------------

If the project already has a ``pyproject.toml`` and ``uv.lock``, move to the
project directory and recreate the environment:

.. code-block:: console

   $ cd <project-dir>
   $ uv sync

``uv sync`` reads ``pyproject.toml`` and ``uv.lock``, creates or updates the
project environment, and installs the locked dependencies. Use this when you
pull the project onto a new HPC location, switch branches, or need to rebuild
the environment before registering the kernel.

If the project has a ``pyproject.toml`` but no lock file yet, run:

.. code-block:: console

   $ uv lock
   $ uv sync

Add or change packages intentionally from the HPC:

.. code-block:: console

   $ uv add scikit-learn
   $ uv add --dev pytest

Then run ``uv sync`` again in any HPC session that should match the updated
project environment.

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

Next steps
----------

After installation, verify that Jupyter can see the new kernel and use
:doc:`manage-kernel` for inspection, renaming, and removal tasks.
