import os
import subprocess
import numpy as np
import nibabel as nib
from dipy.io import read_bvals_bvecs
from dipy.core.gradients import gradient_table

# Load data
data_path = "/90days/uqtshaw/USyd_UQ_dwi_examples/bids/sub-080/dwi/"
data_img_AP = nib.load(os.path.join(data_path, 'sub-080_dir-AP_dwi.nii.gz'))
data_img_PA = nib.load(os.path.join(data_path, 'sub-080_dir-PA_dwi.nii.gz'))

# Load b-values and b-vectors
bvals_AP, bvecs_AP = read_bvals_bvecs(os.path.join(data_path, 'sub-080_dir-AP_dwi.bval'), os.path.join(data_path, 'sub-080_dir-AP_dwi.bvec'))
bvals_PA, bvecs_PA = read_bvals_bvecs(os.path.join(data_path, 'sub-080_dir-PA_dwi.bval'), os.path.join(data_path, 'sub-080_dir-PA_dwi.bvec'))

# Load brain mask
mask_img = nib.load(os.path.join(data_path, 'mask.nii.gz'))
mask = mask_img.get_fdata()

import json

json_file_AP = os.path.join(data_path, 'sub-080_dir-AP_dwi.json')
json_file_PA = os.path.join(data_path, 'sub-080_dir-PA_dwi.json')

with open(json_file_AP) as f:
    json_data_AP = json.load(f)

with open(json_file_PA) as f:
    json_data_PA = json.load(f)

# Extract readout time and phase encoding direction
total_readout_time_AP = json_data_AP['TotalReadoutTime']
total_readout_time_PA = json_data_PA['TotalReadoutTime']
phase_encoding_direction_AP = json_data_AP['PhaseEncodingDirection']
phase_encoding_direction_PA = json_data_PA['PhaseEncodingDirection']

def get_ped_value(ped_str):
    if ped_str == 'i' or ped_str == 'j':
        return 1
    elif ped_str == 'i-' or ped_str == 'j-':
        return -1
    else:
        raise ValueError(f"Invalid phase encoding direction: {ped_str}")

phase_encoding_value_AP = get_ped_value(phase_encoding_direction_AP)
phase_encoding_value_PA = get_ped_value(phase_encoding_direction_PA)

num_volumes_AP = data_img_AP.shape[-1]
num_volumes_PA = data_img_PA.shape[-1]

# Create acqparams_AP.txt and acqparams_PA.txt
acqparams_AP = np.array([0, phase_encoding_value_AP, 0, total_readout_time_AP])
acqparams_PA = np.array([0, phase_encoding_value_PA, 0, total_readout_time_PA])
np.savetxt(os.path.join(data_path, 'acqparams_AP.txt'), acqparams_AP[np.newaxis, :], fmt='%1.6f', delimiter=' ')
np.savetxt(os.path.join(data_path, 'acqparams_PA.txt'), acqparams_PA[np.newaxis, :], fmt='%1.6f', delimiter=' ')

# Create index_AP.txt and index_PA.txt
index_AP = [1] * num_volumes_AP
index_PA = [1] * num_volumes_PA
with open(os.path.join(data_path, 'index_AP.txt'), 'w') as f:
    f.write(" ".join(str(i) for i in index_AP))
    f.write('\n')

with open(os.path.join(data_path, 'index_PA.txt'), 'w') as f:
    f.write(" ".join(str(i) for i in index_PA))
    f.write('\n')


# Run eddy for AP data
eddy_cmd_AP = f"eddy_openmp --imain={os.path.join(data_path, 'sub-080_dir-AP_dwi.nii.gz')} --mask={os.path.join(data_path, 'mask.nii.gz')} --acqp={os.path.join(data_path, 'acqparams_AP.txt')} --index={os.path.join(data_path, 'index_AP.txt')} --bvecs={os.path.join(data_path, 'sub-080_dir-AP_dwi.bvec')} --bvals={os.path.join(data_path, 'sub-080_dir-AP_dwi.bval')} --out={os.path.join(data_path, 'eddy_corrected_data_AP')} --verbose"
subprocess.run(eddy_cmd_AP, shell=True, check=True)

# Run eddy for PA data
eddy_cmd_PA = f"eddy_openmp --imain={os.path.join(data_path, 'sub-080_dir-PA_dwi.nii.gz')} --mask={os.path.join(data_path, 'mask.nii.gz')} --acqp={os.path.join(data_path, 'acqparams_PA.txt')} --index={os.path.join(data_path, 'index_PA.txt')} --bvecs={os.path.join(data_path, 'sub-080_dir-PA_dwi.bvec')} --bvals={os.path.join(data_path, 'sub-080_dir-PA_dwi.bval')} --out={os.path.join(data_path, 'eddy_corrected_data_PA')} --verbose"
subprocess.run(eddy_cmd_PA, shell=True, check=True)

# Load eddy corrected data
corrected_data_img_AP = nib.load(os.path.join(data_path, 'eddy_corrected_data_AP.nii.gz'))
corrected_data_img_PA = nib.load(os.path.join(data_path, 'eddy_corrected_data_PA.nii.gz'))

# Concatenate AP and PA corrected data
concat_corrected_data = np.concatenate((corrected_data_img_AP.get_fdata(), corrected_data_img_PA.get_fdata()), axis=-1)
concat_corrected_data_img = nib.Nifti1Image(concat_corrected_data, corrected_data_img_AP.affine)

# Save concatenated corrected data
nib.save(concat_corrected_data_img, os.path.join(data_path, 'preprocessed_data.nii.gz'))
