"""
Exercise: Download and Deprocess Data in order to get our "raw" sessions.

| Code                                                     | Description                                                                   |
| `run_path('myscript.py')`                                | Run a script in the current python session                                    |
| `run_path('myscript.py', init_globals={'a': 3, 'b': 4})` | Run a script, making variables `a` and `b` with specific value from the start |

Goal: Use `run_path()` to run two key scripts in the workflow, supplying the relevant variables to each script.

"""

# %%
import os  
from pathlib import Path
from runpy import run_path

from tqdm import tqdm  # makes progress bars

os.makedirs('./data', exist_ok=True)

# %% Run Download Data Script: 1_download_data.py
url = "https://uni-bonn.sciebo.de/s/Po9q3wLiNXTxgbj"
nfiles = 3

# run_path() here



# %%  Run Deprocessing Script, once on each file: 2_deprocess_session.py

files = list(Path('./data/original').glob('*.nc'))
for file in tqdm(files, desc=f"Generating Raw Session Files"):
    # run_path() here
    