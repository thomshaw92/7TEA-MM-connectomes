import dipy.reconst.dki as dki
from dipy.data import fetch_cenir_multib
from dipy.core.gradients import gradient_table
from dipy.io.gradients import read_bvals_bvecs
from dipy.io.image import load_nifti, save_nifti

# Load your preprocessed data
data, affine = load_nifti('your_preprocessed_dwi.nii.gz')
bvals, bvecs = read_bvals_bvecs('your_bvals_file.bval', 'your_bvecs_file.bvec')
gtab = gradient_table(bvals, bvecs)

# Fit the DKI model
dkimodel = dki.DiffusionKurtosisModel(gtab)
dkifit = dkimodel.fit(data)

# Save DKI metrics
save_nifti('MK.nii.gz', dkifit.mk(0, 3), affine)
save_nifti('AK.nii.gz', dkifit.ak(0, 3), affine)
save_nifti('RK.nii.gz', dkifit.rk(0, 3), affine)

