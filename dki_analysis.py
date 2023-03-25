import os
import numpy as np
import nibabel as nib

from dipy.core.gradients import gradient_table
from dipy.reconst.dki import DiffusionKurtosisModel


data_path = "/90days/uqtshaw/USyd_UQ_dwi_examples/bids/sub-080/dwi/"

# Load bvals and bvecs
bvals_AP_path = os.path.join(data_path, 'sub-080_dir-AP_dwi.bval')
bvals_PA_path = os.path.join(data_path, 'sub-080_dir-PA_dwi.bval')
bvecs_AP_path = os.path.join(data_path, 'sub-080_dir-AP_dwi.bvec')  
bvecs_PA_path = os.path.join(data_path, 'sub-080_dir-PA_dwi.bvec')  


bvals_AP = np.loadtxt(bvals_AP_path)
bvals_PA = np.loadtxt(bvals_PA_path)
bvecs_AP = np.loadtxt(bvecs_AP_path)
bvecs_PA = np.loadtxt(bvecs_PA_path)
dwi_AP_path = os.path.join(data_path, 'sub-080_dir-AP_dwi.nii.gz')
dwi_PA_path = os.path.join(data_path, 'sub-080_dir-PA_dwi.nii.gz')

dwi_AP = nib.load(dwi_AP_path)
dwi_PA = nib.load(dwi_PA_path)

print("Shape of dwi_AP:", dwi_AP.shape)
print("Shape of dwi_PA:", dwi_PA.shape)

bvecs = np.concatenate((bvecs_AP, bvecs_PA), axis=1)  # Concatenate along columns

# Normalize bvecs
bvecs_normalized = bvecs / (np.linalg.norm(bvecs, axis=0) + np.finfo(float).eps)

# Check if the bvecs are unit length
norms = np.linalg.norm(bvecs_normalized, axis=0)
if not np.allclose(norms, np.ones_like(norms), rtol=1e-3):
    print("WARNING: The bvecs are not unit length.")

# Check if the bvecs are unit length
print("Norm of concatenated bvecs (should be close to 1):\n", np.linalg.norm(bvecs_normalized, axis=0))

bvecs = bvecs_normalized
bvals = bvals_AP.tolist() + bvals_PA.tolist()

print("Shape of bvals:", len(bvals))
print("Shape of bvecs:", bvecs.shape)

gtab = gradient_table(bvals, bvecs, atol=1e-2)


def run_dki(preprocessed_data_path, mask_path, output_prefix):
    preprocessed_data = nib.load(preprocessed_data_path).get_fdata()
    mask_img = nib.load(mask_path)
    mask_data = mask_img.get_fdata()

    gtab = gradient_table(bvals, bvecs)
    dki_model = DiffusionKurtosisModel(gtab)
    dki_fit = dki_model.fit(preprocessed_data, mask=mask_data)

    # Save DKI metrics
    fa_img = nib.Nifti1Image(dki_fit.fa, mask_img.affine)
    nib.save(fa_img, os.path.join(data_path, f"{output_prefix}_dki_fa.nii.gz"))

    md_img = nib.Nifti1Image(dki_fit.md, mask_img.affine)
    nib.save(md_img, os.path.join(data_path, f"{output_prefix}_dki_md.nii.gz"))

    mk_img = nib.Nifti1Image(dki_fit.mk(0, 3), mask_img.affine)
    nib.save(mk_img, os.path.join(data_path, f"{output_prefix}_dki_mk.nii.gz"))

    ak_img = nib.Nifti1Image(dki_fit.ak(0, 3), mask_img.affine)
    nib.save(ak_img, os.path.join(data_path, f"{output_prefix}_dki_ak.nii.gz"))

    rk_img = nib.Nifti1Image(dki_fit.rk(0, 3), mask_img.affine)
    nib.save(rk_img, os.path.join(data_path, f"{output_prefix}_dki_rk.nii.gz"))

    print(f"DKI metrics saved for {output_prefix}.")

mask_path = os.path.join(data_path, "mask.nii.gz")

# Convert MRtrix3 mif file to NIfTI
mrtrix_mif_path = os.path.join(data_path, "sub-080_ses-01_space-dwi_desc-dwi_preproc.mif")
mrtrix_nifti_path = os.path.join(data_path, "mrtrix_preprocessed.nii.gz")
os.system(f"mrconvert {mrtrix_mif_path} {mrtrix_nifti_path}")

# Run DKI on the preprocessed data
preprocessed_data_path = os.path.join(data_path, "preprocessed_data.nii.gz")
run_dki(preprocessed_data_path, mask_path, "preprocessed")

# Run DKI on the MRtrix3 preprocessed data
run_dki(mrtrix_nifti_path, mask_path, "mrtrix_preprocessed")

print("DKI metrics saved successfully.")