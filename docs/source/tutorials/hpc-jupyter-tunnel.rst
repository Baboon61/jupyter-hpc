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
* ``uv`` available on the HPC for the JupyterLab server and uv-managed Python
  kernels.
* Conda, Mamba, or Micromamba available on the HPC for conda-managed Python or
  R kernels.
* VS Code or Cursor installed on the workstation with Jupyter support enabled.
* A Python project with a ``pyproject.toml`` file, if you want a uv-managed
  Python kernel.
* Access to the HPC filesystem location that contains the protected data.

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

Before starting JupyterLab, create the kernels that notebooks will use on the
HPC. Choose the setup recipe that matches your project:

* :doc:`/reference/install-uv-python-kernel`
* :doc:`/reference/install-conda-kernels`

The short version is:

* Use ``uv`` for Python projects that should be driven by ``pyproject.toml``.
* Use conda, Mamba, or Micromamba for named Python environments or R kernels.
* Register each environment as a Jupyter kernel before connecting from VS Code
  or Cursor.

Log in to the HPC and move to the project directory:

.. code-block:: console

   $ ssh <hpc-login>
   $ cd <project-dir>

The linked recipes walk through installation from ``curl`` or installer
download through kernel registration.

.. note::

   This tutorial uses Jupyter with an R kernel instead of RStudio because the
   two tools expose remote execution differently. VS Code and Cursor can attach
   a local notebook file to a remote Jupyter kernel, so local editing and
   HPC-side execution stay separated. RStudio Server provides its own web IDE
   and R session together; it does not normally act as a kernel backend for
   local ``.R`` or ``.Rmd`` files opened in VS Code or Cursor.

Allocate a SLURM job
--------------------

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

Keep this terminal open. The reported hostname is the node that the SSH tunnel
must reach.

Start JupyterLab on the compute node
------------------------------------

From inside the SLURM allocation, start JupyterLab without opening a browser:

.. code-block:: console

   $ cd <project-dir>
   $ uv run --with jupyter jupyter lab \
       --no-browser \
       --ip=127.0.0.1 \
       --port=<remote-port>

Jupyter prints a URL that includes a token. Keep the token private. Do not paste
it into source files, shared tickets, commits, or chat logs.

Create the SSH tunnel from the workstation
------------------------------------------

In a workstation terminal, forward a local port to the JupyterLab port on the
HPC compute node. Many HPC systems require a jump through the login node:

.. code-block:: console

   $ ssh -N \
       -L <local-port>:<compute-node>:<remote-port> \
       <hpc-login>

For example, if JupyterLab is listening on port ``8888`` on compute node
``cn042``:

.. code-block:: console

   $ ssh -N -L 8888:cn042:8888 login.cluster.example

Keep the tunnel running while you use the notebooks.

Connect from VS Code or Cursor
------------------------------

In VS Code or Cursor:

1. Open your local notebook project.
2. Open the command palette.
3. Run ``Jupyter: Specify Jupyter Server for Connections``.
4. Choose an existing server or enter the forwarded URL:

   .. code-block:: text

      http://127.0.0.1:<local-port>/?token=<token>

5. Open a notebook and select the ``Python (ai-bunker)`` or ``R (ai-bunker)``
   kernel.

The notebook file is edited locally, but cells run in the selected kernel on the
HPC. Paths such as ``<data-dir>`` are resolved by the remote kernel, not by the
workstation.

Switch kernels in a notebook
----------------------------

Each notebook can use a different registered kernel. Use the kernel picker in
VS Code or Cursor to switch between Python and R, or between project
environments. If you add another uv, conda, or R environment later, repeat the
kernel registration step from the relevant setup recipe with a new ``--name`` or
``name`` value and a new display name.

Restart Jupyter or refresh the kernel list if the new kernel does not appear.

Install packages intentionally
------------------------------

For uv-managed Python kernels, prefer changing the project environment from a
terminal on the HPC:

.. code-block:: console

   $ uv add pandas matplotlib

For temporary or exploratory packages, use ``uv pip install`` inside the project
environment with care:

.. code-block:: console

   $ uv pip install <package>

For conda-managed Python kernels, install packages into the named conda
environment:

.. code-block:: console

   $ conda install -n py-ai-bunker -c conda-forge <package>

For R kernels, prefer installing packages into the conda environment from an HPC
terminal:

.. code-block:: console

   $ conda install -n r-ai-bunker -c conda-forge r-<package>

If a package is not available from the approved conda channels, follow your
site's policy for installing R packages from inside the activated conda
environment:

.. code-block:: console

   $ conda activate r-ai-bunker
   $ R -e "install.packages('<package>')"

Avoid ad hoc package installation from notebook cells unless your team has
agreed that notebooks may mutate their execution environment.

Keep Codex away from the HPC
----------------------------

If your policy requires AI tools to stay away from the HPC, treat this as a
technical boundary, not only as a working convention. Codex should edit local
code and documentation only. It should not receive HPC hostnames, SSH commands,
Jupyter tokens, protected paths, cell outputs, or terminal access that can reach
the cluster.

The strongest pattern is to separate the AI coding environment from the HPC
access environment:

* Run Codex in a local-only workspace that contains code, documentation, and
  synthetic examples only.
* Run the SSH tunnel and the remote Jupyter connection from a different terminal,
  IDE window, operating-system account, VM, or managed workstation profile that
  Codex cannot access.
* Do not run Codex from a VS Code or Cursor window connected through Remote SSH
  to the HPC.
* Do not install or run Codex on the HPC login node, compute node, or shared
  project filesystem.
* Paste the Jupyter token only into the Jupyter connection prompt. Do not save it
  in ``.env`` files, notebooks, source files, shell history examples, issue
  comments, or chat messages.

On Windows, a practical setup is to use a separate local account for Codex that
has no HPC SSH keys, no HPC SSH config, and no mounted protected data. Create the
account from an Administrator PowerShell:

.. code-block:: powershell

   PS> $password = Read-Host "Password for codex-local" -AsSecureString
   PS> New-LocalUser `
       -Name "codex-local" `
       -Password $password `
       -Description "Local AI coding account without HPC credentials"

Then open the repository from that account and confirm that the account cannot
see your normal SSH material:

.. code-block:: powershell

   PS> whoami
   PS> Test-Path "$env:USERPROFILE\.ssh"
   PS> Get-ChildItem Env: | Where-Object Name -match "SSH|JUPYTER|TOKEN|HPC"

The expected result is that ``whoami`` shows the isolated account, ``.ssh`` is
missing or contains no HPC credentials, and the environment does not expose
tokens, SSH agent sockets, or HPC-specific variables.

Avoid running Codex in the same operating-system account that owns the SSH
keys, SSH agent, Jupyter token, and open tunnel. If Codex can start shell
commands in that account, it may be able to call the same ``ssh`` executable,
read the same local files, or connect to the same ``127.0.0.1`` tunnel as the
human user.

For a dedicated Codex VM, sandbox, workstation, or centrally managed profile
with its own network policy, add a network block that applies to the whole
isolated environment. For example, block SSH to the HPC login node from an
Administrator PowerShell:

.. code-block:: powershell

   PS> New-NetFirewallRule `
       -DisplayName "Block isolated Codex environment to HPC SSH" `
       -Direction Outbound `
       -Action Block `
       -Protocol TCP `
       -RemoteAddress "<hpc-login-ip-or-cidr>" `
       -RemotePort 22

If the isolated environment should never use the forwarded Jupyter port, block
that local port there as well:

.. code-block:: powershell

   PS> New-NetFirewallRule `
       -DisplayName "Block isolated Codex environment to local Jupyter tunnel" `
       -Direction Outbound `
       -Action Block `
       -Protocol TCP `
       -RemoteAddress 127.0.0.1 `
       -RemotePort <local-port>

Do not use a machine-wide firewall rule for ``<hpc-login>`` or
``127.0.0.1:<local-port>`` if the same workstation still needs VS Code or Cursor
to create the tunnel. Machine-wide rules can block the notebook workflow itself.
In that case, put Codex in a separate VM, sandbox, or managed profile where the
network block does not affect the approved Jupyter session.

Verify the boundary from the Codex environment, not from your regular HPC
terminal:

.. code-block:: powershell

   PS> ssh -o BatchMode=yes <hpc-login>
   PS> Test-NetConnection <hpc-login> -Port 22
   PS> Test-NetConnection 127.0.0.1 -Port <local-port>

For a strict separation, these checks should fail from the Codex environment.
The same checks may succeed from the separate terminal or account that you use
for the approved HPC tunnel.

Before asking Codex to edit or review notebook work, strip sensitive outputs and
avoid giving it remote execution details:

.. code-block:: powershell

   PS> jupyter nbconvert --ClearOutputPreprocessor.enabled=True `
       --inplace path\to\notebook.ipynb

Keep prompts to Codex focused on local code structure, tests with synthetic data,
documentation wording, and review of non-sensitive outputs. Execute real Python
or R cells against protected data yourself through the approved HPC Jupyter
kernel.

Security checklist
------------------

Before committing or sharing notebook work:

* Confirm protected datasets were read from HPC paths only.
* Clear outputs that may contain sensitive values, previews, or derived records.
* Keep Jupyter tokens out of committed files and shared messages.
* Stop JupyterLab when the session ends.
* Close the SSH tunnel after stopping the notebook server.
* Cancel the SLURM allocation if it remains active.

Troubleshooting
---------------

If the browser or IDE cannot connect, check that Jupyter is still running, the
SLURM allocation is still active, and the tunnel points to the compute node
reported by ``hostname``.

If the notebook cannot see protected files, verify that the selected kernel is
the HPC kernel and that the path exists on the HPC filesystem.

If the expected kernel is missing, rerun the ``ipython kernel install`` command
or the ``IRkernel::installspec`` command from the HPC project and refresh the
Jupyter server connection.

See :doc:`/reference/hpc-jupyter-commands` for reusable JupyterLab command
templates and :doc:`/concepts/execution-boundaries` for the execution and
data boundary model.
