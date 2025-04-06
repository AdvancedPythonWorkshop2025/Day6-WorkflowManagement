# %%
import os  
from pathlib import Path
from runpy import run_path

from tqdm import tqdm  # makes progress bars

os.chdir(Path(__file__).parent)  # Set current directory to project root.

os.makedirs('./data', exist_ok=True)

# %% Run Download Data Script
url = "https://uni-bonn.sciebo.de/s/Po9q3wLiNXTxgbj"
nfiles = 3
run_path('scripts/1_download_data.py', init_globals={'nfiles': nfiles, 'url': url})


# %%  Run Deprocessing Task

files = list(Path('./data/original').glob('*.nc'))
for file in tqdm(files, desc=f"Generating Raw Session Files"):
    run_path('scripts/2_deprocess_session.py', init_globals={'file': file})
    