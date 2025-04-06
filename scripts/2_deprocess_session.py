# %% Import and Setup
from pathlib import Path
import os

import numpy as np
from scipy import io
from tqdm import tqdm
import xarray as xr
import xmltodict

os.chdir(Path(__file__).parent.parent)
os.makedirs('data/raw', exist_ok=True)

# %% Set Script Parameters
if 'file' in globals():
    assert file.exists()
else:
    files = list(Path(r'.\data\original').glob('*.nc'))
    list(files)
    file = files[0]

file

# %% Load Processed File
dset = xr.load_dataset(file)
dset

# %% Get Session Metadata, Make Filename out of It

session = \
    dset.attrs['session_date'].replace('-', '') + '_' + \
    dset.attrs['mouse'].lower() + '_' + \
    'steinmetz'

os.makedirs(f'data/raw/{session}', exist_ok=True)

session

# %% Get LFP Data
lfp = dset.lfp
lfp

# %% Write LFP to binary file + a text timestamp file + a channel map text file
lfp2 = lfp.transpose('trial', 'time', 'brain_area_lfp')  # this order mimics saving all channels over time.

lfp_recs = lfp2.values.tobytes()
os.makedirs(f'data/raw/{session}/lfp', exist_ok=True)
with open(f'data/raw/{session}/lfp/recording.bin', 'wb') as f:
    f.write(lfp_recs)

times = np.arange(lfp2.time.size * lfp2.trial.size) * .01
(times * 1000).astype(int).tofile(f'data/raw/{session}/lfp/sampletimes.dat',sep='\n')

with open(f"data/raw/{session}/lfp/regionmap.txt", 'w') as f:
    for idx, region in enumerate(lfp.brain_area_lfp.values.tolist(), start=1):
        f.write(f"CHAN{idx:03d}\t{region}\n")


# %%  Write Experimenter- and Subject-Controlled events as Named Trigger Timestamps
trial_start_times = ((lfp2.trial - 1) * lfp2.time.max()).values
trial_start_times

triggers = {}
for tstamp in trial_start_times:
    triggers[tstamp] = 'TBEG'

for tstamp, stimon in zip(trial_start_times, dset.stim_onset.values):
    triggers[tstamp + stimon] = 'STIM'
    
for tstamp, active_resp in zip(trial_start_times, dset.active_trials.values):
    if active_resp:
        triggers[tstamp + np.random.randint(5, 200) / 100] = 'RESP'

for tstamp, gocue in zip(trial_start_times, dset.gocue.values):
    if not np.isnan(gocue):
        triggers[tstamp + gocue] = 'GOCU'

for tstamp, ftime, ftype in zip(trial_start_times, dset.feedback_time.values, dset.feedback_type.values):
    if not np.isnan(ftype):
        if ftype == -1:
            triggers[tstamp + ftime] = 'FNEG'
        elif ftype == 1:
            triggers[tstamp + ftime] = 'FPOS'
        else:
            raise ValueError(f"Couldn't process {ftype}")
        

for tstamp, rtime, rtype in zip(trial_start_times, dset.response_time.values, dset.response_type.values):
    if not np.isnan(rtype):
        if rtype == -1:
            triggers[tstamp + rtime] = 'RSPL'
        elif rtype == 1:
            triggers[tstamp + rtime] = 'RSPR'
        elif rtype == 0:
            triggers[tstamp + rtime] = 'RSPN'
        else:
            raise ValueError(f"Couldn't process {rtype}")


for time, nlicks in zip(times, dset.licks.values.flatten()):
    for _ in range(nlicks):
        triggers[time + np.random.randint(0, 11) / 1000] = 'LICK'

with open(f"data/raw/{session}/triggers.dat", 'w') as f:
    for tstamp, label in sorted(triggers.items()):
        f.write(f"{label}\t{int(tstamp * 1000)}\t0\t0\n")

f"{len(triggers)} Triggers in Total"

# %% Put Stimulus Details as a CSV File
stimuli = dset[['contrast_left', 'contrast_right']].to_dataframe()
stimuli.to_csv(f'data/raw/{session}/stimuli.csv')
stimuli


# %% Save Wheel Movement Directions as a Matlab file (let's pretend a matlab script was doing wheel processing.)
wheel = dset['wheel'].values.flatten()
times2 = (times * 1000).astype(np.uint16)
io.savemat(f'data/raw/{session}/wheel.mat', mdict={'wheel': wheel, 'time': times2})

# %% Save eye-tracking data as chunked XML files (say, from a program processing image frames)
os.makedirs(f"data/raw/{session}/eye_tracking", exist_ok=True)

nfile = 0
nrow = 0
for i, (time, (idx, row)) in tqdm(enumerate(zip(times, dset[['pupil_x', 'pupil_y', 'pupil_area', 'face']].to_dataframe().iterrows()), start=1)):
    if nrow > 15000:
        xmltodict.unparse(xml_dict, f, pretty=True)
        f.close()
        nrow = 0
    if nrow == 0:
        xml_dict = {'root': {}}
        nfile += 1
        f = open(f"data/raw/{session}/eye_tracking/CHUNK{nfile:05d}.xml", 'w')
    
    dd = row.to_dict()
    xml_dict['root'][f'frame{i:05d}'] = {
        'time': {
            "@name": "Clock Time",
            "@units": "msecs",
            "#text": str(int(time * 1000)),
        },
        'pupilx': {
            "@name": "Pupil X Position",
            "@units": "px",
            "#text": str(dd['pupil_x']),
        },
        'pupily': {
            "@name": "Pupil Y Position",
            "@units": "px",
            "#text": str(dd['pupil_y']),
        },
        'pupil_area': {
            "@name": "Pupil Area",
            "@units": "px^2",
            "#text": str(dd['pupil_area']),
        },
    }
    nrow += 1

xmltodict.unparse(xml_dict, f, pretty=True)
f.close()
    
