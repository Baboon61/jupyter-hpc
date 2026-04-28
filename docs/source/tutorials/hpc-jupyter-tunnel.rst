Run JupyterLab on an HPC through an SSH tunnel
==============================================

This walkthrough shows how to run JupyterLab on a SLURM-managed HPC compute
node, tunnel the server to a workstation, and connect VS Code or Cursor to the
remote Jupyter server. The notebook editor stays local, while code execution
and protected data access happen on the HPC.

Architecture
------------

The workflow uses three layers:

* **Workstation**: VS Code or Cursor opens notebooks and provides AI assistance.
* **SSH tunnel**: a local port forwards browser and notebook traffic to the HPC.
* **HPC compute node**: JupyterLab and the selected Python or R kernel
  run near the protected data.

Notebook files can live in your local project if your workflow only stores code,
queries, and non-sensitive outputs. Any notebook that reads protected data
must run its code in a kernel on the HPC. In Jupyter, the kernel process opens
files, imports packages, executes cell code, and resolves data paths. The local
editor only sends code to that remote runtime.

Prerequisites
-------------

Before starting, make sure you have:

* SSH access to the HPC login node.
* A SLURM partition that allows interactive or batch jobs.
* Access to the HPC filesystem location that contains the protected data.
* VS Code or Cursor installed on the workstation with Jupyter support enabled.

The examples below use placeholders. Replace them for your site:

.. code-block:: text

   <hpc-login>        Login node hostname, such as login.cluster.example
   <account>          SLURM account or allocation name
   <partition>        SLURM partition or queue
   <project-dir>      Project directory on the HPC
   <data-dir>         Protected data directory on the HPC
   <local-port>       Port opened on the workstation, such as 8888
   <remote-port>      Port opened by JupyterLab on the HPC, such as 8888

Prepare notebook kernels on the HPC
-----------------------------------

In Jupyter, a kernel is the process that runs notebook cells. It imports
packages, opens files, keeps variables in memory, and returns results to the
notebook interface. In this workflow, the kernel runs on the HPC so protected
data is read by an HPC process, while VS Code or Cursor remains the local
editing interface.

Before starting JupyterLab, create the kernels that notebooks will use on the
HPC. For python centered kernels, please use ``uv``, for any other kernels like R, please use ``conda`` or ``mamba``.
The linked recipes show how to set up kernels for Python and R:

.. grid:: 2

   .. grid-item-card::
      :link: /references/install-uv-python-kernel
      :link-type: doc

      .. image:: /_static/uv-logo.png
         :alt: uv logo
         :align: right
         :width: 55

      Create a Python kernel from a ``uv`` managed project and register it for
      remote Jupyter use on the HPC.

      Best for :bdg-success:`Python` \      
      Environment manager :bdg-info:`uv`

   .. grid-item-card::
      :link: /references/install-conda-kernels
      :link-type: doc

      .. image:: /_static/conda-logo.png
         :alt: conda logo
         :align: right
         :width: 60

      Create Python or R kernels from ``conda`` managed project and register it
      for remote Jupyter use on the HPC.

      Best for :bdg-success:`Python` :bdg-success:`R` \
      Environment manager :bdg-info:`conda` :bdg-info:`mamba`

.. note::

   This tutorial uses Jupyter with an R kernel instead of RStudio because the
   two tools expose remote execution differently. VS Code and Cursor can attach
   a local notebook file to a remote Jupyter kernel, so local editing and
   HPC-side execution stay separated. RStudio Server provides its own web IDE
   and R session together; it does not normally act as a kernel backend for
   local ``.R`` or ``.Rmd`` files opened in VS Code or Cursor.

Allocate a SLURM job
--------------------

Through a terminal, log in to the HPC and move to the project directory:

.. code-block:: console

   $ ssh <hpc-login>

Start an interactive job for the JupyterLab server. The exact resource request
depends on your HPC policy and workload:

.. code-block:: console

   $ salloc \
       --account=<account> \
       --partition=<partition> \
       --time=02:00:00 \
       --cpus-per-task=4 \
       --mem=16G

After the allocation starts, identify the compute node:

.. code-block:: console

   $ hostname

.. important::

   Keep this terminal open.
   The reported hostname is the node that the SSH tunnel
   must reach.

.. seealso::

   If your HPC workflow prefers batch submission, you can start the Jupyter
   instance with ``sbatch`` instead of ``salloc``. See
   :doc:`../references/hpc-jupyter-commands` for a reusable batch job example.

.. note::

   This walkthrough uses `SLURM <https://slurm.schedmd.com/>`__ for concrete
   examples. If your HPC uses another scheduler such as
   `SGE <https://en.wikipedia.org/wiki/Oracle_Grid_Engine>`__ or
   `HTCondor <https://htcondor.readthedocs.io/>`__, use the equivalent job
   submission pattern from your local infrastructure manual and follow your
   site's scheduler-specific guidance.

Start JupyterLab on the compute node
------------------------------------

From inside the SLURM allocation, start JupyterLab without opening a browser:

.. tabs::

   .. tab:: uv

      For a uv-managed project:

      .. code-block:: console

         $ cd <project-dir>
         $ uv run --with jupyter jupyter lab \
             --no-browser \
             --ip=127.0.0.1 \
             --port=<remote-port>

   .. tab:: conda

      For a conda-managed environment, activate the environment first and then
      launch JupyterLab:

      .. code-block:: console

         $ cd <project-dir>
         $ conda activate py-ai-bunker
         $ jupyter lab \
             --no-browser \
             --ip=127.0.0.1 \
             --port=<remote-port>

.. note::

   Jupyter prints a URL that includes a token. Keep the token private. Do not paste
   it into source files, shared tickets, commits, or chat logs.

Create the SSH tunnel from the workstation
------------------------------------------

In a workstation terminal, forward a local port to the JupyterLab port on the
HPC compute node. Many HPC systems require a jump through the login node:

.. tabs::

   .. tab:: Main method

      .. code-block:: console

         $ ssh -N \
            -L <local-port>:<compute-node>:<remote-port> \
            <hpc-login>

      For example, if JupyterLab is listening on port ``8888`` on compute node
      ``cn042``:

      .. code-block:: console

         $ ssh -N -L 8888:cn042:8888 login.cluster.example

   .. tab::  Alternative method

      .. code-block:: console

         $ ssh -t \
            -t <hpc-login> \
            -L <local-port>:127.0.0.1:<remote-port> \
            ssh <compute-node> \
            -L <local-port>:127.0.0.1:<remote-port>
            
      For example, if JupyterLab is listening on port ``8888`` on compute node
      ``cn042``:

      .. code-block:: console

         $ ssh -t -t login.cluster.example -L 8888:127.0.0.1:8888 ssh cn042 -L 8888:127.0.0.1:8888

.. important::

   Keep the tunnel running while you use the notebooks.