# %%
import os  
from pathlib import Path
from runpy import run_path

from tqdm import tqdm  # makes progress bars

os.chdir(Path(__file__).parent)  # Set current directory to project root.

# %%

files = list(Path('./data/original').glob('*.nc'))
files = files[:5]
for file in tqdm(files, desc=f"Generating Raw Session Files"):
    run_path('scripts/deprocess_session.py', init_globals={'file': file})
    