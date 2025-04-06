"""
Exercise: Run the "Extract" notebooks on each of the raw datasets.

1) Se
t a notebook cell with the "parameters" cell tag.  The variables in this cell can be overridden.

2) Run the notebook using papermill's `execute_notebook()` function:
`
pm.execute_notebook(
   'path/to/input.ipynb',
   'path/to/output.ipynb',
   parameters=dict(alpha=0.6, ratio=0.1)
)
`

Papermill Docs: https://papermill.readthedocs.io/en/latest/

"""

import papermill as pm