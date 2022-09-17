#!/bin/bash

#run micapipe on 7TEA data
#TBS 20220917
for subjName in `cat /30days/uqtshaw/7TEA/subjnames.csv` ; do

singularity run --cleanenv \
    -B /30days/uqtshaw/7TEA/bids:/bids_dataset:ro \
    -B /30days/uqtshaw/7TEA/bids/derivatives:/output_directory \
    -B /30days/uqtshaw/7TEA/micapipe_work_dir:/tmp \
    -B /data/lfs2/uqtshaw/license.txt:/opt/freesurfer-6.0.0/license.txt \
    /data/lfs2/uqtshaw/micapipe-latest.simg \
     -bids ./bids/ \
     -out derivatives \
     -sub P0020 \
     -ses ses-01 \
     -proc_structural \
     -proc_freesurfer \
     -hires \
     -post_structural \
     -MPC \
     -microstructural_img ./bids/sub-P0020/ses-01/dwi/sub-P0020_ses-01_T1map.nii.gz \
     -microstructural_reg ./bids/sub-P0020/ses-01/dwi/sub-P0020_ses-01_IV1.nii.gz \
     -proc_dwi \
     -dwi_main ./bids/sub-P0020/ses-01/dwi/sub-P0020_ses-01_acq-b1000_dir-AP_run-1_dwi.nii.gz,./bids/sub-P0020/ses-01/dwi/sub-P0020_ses-01_acq-b2500_dir-AP_run-1_dwi.nii.gz \
     -dwi_rpe ./bids/sub-P0020/ses-01/dwi/sub-P0020_ses-01_acq-b0_dir-PA_run-1_dwi.nii.gz \
     -SC \
     -tracts 20M \
     -proc_rsfmri \
     -mainScanStr sub-P0020_ses-01_rest_run_bold.nii.gz \
     -regress_WM_CSF \
     -noFIX \
     -regAffine \
     -GD \
     -Morphology \
     -threads 40 \
     -QC_subj

