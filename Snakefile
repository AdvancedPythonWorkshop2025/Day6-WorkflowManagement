"""
Exercise 1: Delete the data/original folder and run the snakemake workflow in this file.


| Code                               |
| ---------------------------------- |
| `snakemake --cores 1`              |
| `snakemake --rulegraph mermaid-js  |


Exercise 2: Add the deproces_sessions rule.

Starter for Using Snakemake: https://snakemake.readthedocs.io/en/stable/snakefiles/rules.html


| Code                               |
| ---------------------------------- |
| `output: "data/myfile.txt"`        |
| `output: directory("data/folder")` |
| `params: x = 3`                    |
| `run: my_python_code()`            |
| `python: "my_script.py"`           |
| `shell: "python my_script.py"      |


Exercise 3: Add rules for each of the extract notebooks, using papermill.

"""

########### Setup

import pandas as pd
# Get all expected sessions from the sessions spreadsheet.
sessions = pd.read_excel('data/sessions.xlsx').to_dict('records')
# print(sessions)

# Create lists of values that can be used in Snakemake's expand() function, for wildcard use
nfiles = 2
mice = [sess['mouse'] for sess in sessions]
researchers = [sess['researcher'] for sess in sessions]
dates = [sess['date'] for sess in sessions]


######### Rules

rule all:
    input:
        expand("data/original/{researcher}_{date}_{mouse}.nc", zip, researcher=researchers[:nfiles], date=dates[:nfiles], mouse=mice[:nfiles])


rule download_data:
    output: 
        "data/original/{researcher}_{date}_{mouse}.nc"
    params:
        nfiles=nfiles
    run:
        from runpy import run_path
        run_path(
            'scripts/1_download_data.py', 
            init_globals={
                'url': "https://uni-bonn.sciebo.de/s/Po9q3wLiNXTxgbj",
                'nfiles': params.nfiles
            }
        )


