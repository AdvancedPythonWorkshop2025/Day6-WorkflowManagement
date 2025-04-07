# %%
import os
from pathlib import Path

import owncloud
from tqdm import tqdm

os.chdir(Path(__file__).parent.parent)


# %% Set Script Parameters
if not 'url' in globals():
    url = "https://uni-bonn.sciebo.de/s/Po9q3wLiNXTxgbj"
if not 'nfiles' in globals():
    nfiles = 2
    
nfiles, url

# %% Download Data
client = owncloud.Client.from_public_link(url)
os.makedirs('data/original', exist_ok=True)
for file in tqdm(client.list('/')[:nfiles], desc="Downloading Files"):
    client.get_file(file, f"data/original/{file.name.lower().replace('-', '')}")

