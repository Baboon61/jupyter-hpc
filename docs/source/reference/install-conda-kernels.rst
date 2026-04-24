Install conda and create Python or R kernels
============================================

Use this recipe on the HPC when you want Jupyter kernels backed by conda
environments. It starts with installing Miniforge and ends with named Python and
R kernels that VS Code or Cursor can select through the remote Jupyter server.

Install Miniforge
-----------------

Miniforge is a conda-forge distribution that provides ``conda`` and uses the
``conda-forge`` channel by default. Download the installer from the official
conda-forge Miniforge releases:

.. code-block:: console

   $ curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"

Run the installer interactively:

.. code-block:: console

   $ bash Miniforge3-$(uname)-$(uname -m).sh

For a non-interactive install, use the batch flag:

.. code-block:: console

   $ bash Miniforge3-$(uname)-$(uname -m).sh -b

Restart the shell, or initialize conda for the current shell according to the
installer output. Then confirm conda is available:

.. code-block:: console

   $ conda --version

See the official `Miniforge documentation <https://github.com/conda-forge/miniforge>`__
for platform-specific installers, shell initialization, and non-interactive
options.

Create a Python kernel environment
----------------------------------

Create a Python environment with ``ipykernel`` and any approved project
packages:

.. code-block:: console

   $ conda create -n py-ai-bunker -c conda-forge python ipykernel pandas matplotlib

Activate it and register it as a Jupyter kernel:

.. code-block:: console

   $ conda activate py-ai-bunker
   $ python -m ipykernel install \
       --user \
       --name py-ai-bunker \
       --display-name "Python (ai-bunker)"

Create an R kernel environment
------------------------------

Create an R environment with ``IRkernel``:

.. code-block:: console

   $ conda create -n r-ai-bunker -c conda-forge r-base r-irkernel

Install any approved R packages from conda-forge:

.. code-block:: console

   $ conda install -n r-ai-bunker -c conda-forge r-tidyverse

Activate the environment and register it as a Jupyter kernel:

.. code-block:: console

   $ conda activate r-ai-bunker
   $ R -e "IRkernel::installspec(name = 'r-ai-bunker', displayname = 'R (ai-bunker)', user = TRUE)"

If a package is not available from approved conda channels, follow your site's
policy for installing R packages from inside the activated conda environment:

.. code-block:: console

   $ conda activate r-ai-bunker
   $ R -e "install.packages('<package>')"

Verify the kernels
------------------

List available kernels from the HPC:

.. code-block:: console

   $ jupyter kernelspec list

Start or refresh the remote Jupyter server, then select ``Python (ai-bunker)``
or ``R (ai-bunker)`` from VS Code or Cursor.
