ai-bunker documentation
=======================

**ai-bunker** is a practical guide for running AI-assisted notebook
development against protected `HPC <https://en.wikipedia.org/wiki/High-performance_computing>`__
data. The main workflow starts
`JupyterLab <https://jupyterlab.readthedocs.io/>`__ on an HPC compute node,
forwards it through an `SSH <https://www.openssh.com/>`__ tunnel, and connects
from a local IDE like `VS Code <https://code.visualstudio.com/>`__ or
`Cursor <https://cursor.com/>`__. The remote Jupyter server can expose Python
or R kernels while keeping execution near the protected data.

The key boundary is intentional: data and kernel execution stay on the HPC,
while the workstation provides the editing experience and AI assistance.

.. see also::

   Background and command templates are available in the concepts and references sections.

.. warning::

   This project is under active development.

.. toctree::
   :caption: Tutorials
   :hidden:

   tutorials/hpc-jupyter-tunnel
   tutorials/load-kernel-from-ide

.. toctree::
   :caption: Concepts
   :hidden:

   concepts/execution-boundaries

.. toctree::
   :caption: References
   :hidden:

   references/install-uv-python-kernel
   references/install-conda-kernels
   references/manage-kernel
   references/hpc-jupyter-commands
