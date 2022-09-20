#!/bin/bash

#run micapipe on 7TEA data
#TBS 20220917
for subjName in `cat /30days/uqtshaw/7TEA/scripts/7TEA-MM-connectomes/subjnames.csv` ; do
    singularity_image="/data/lfs2/uqtshaw/micapipe-latest.simg"
    fastsurfer_simg="/data/lfs2/uqtshaw/fastsurfer.sif"
    base_dir="/30days/uqtshaw/7TEA"
    if [[ ! -e ${base_dir}/bids/derivatives/freesurfer/${subjName}_ses-01/scripts/recon-all.done ]] ; then
	singularity exec -B ${base_dir}/bids:/data \
                    -B ${base_dir}/bids/derivatives/freesurfer/:/output \
                    -B /data/lfs2/uqtshaw/:/fs_license \
                    ${fastsurfer_simg} \
                    /fastsurfer/run_fastsurfer.sh \
                    --fs_license /fs_license/license.txt \
                    --t1 /data/${subjName}/ses-01/anat/${subjName}_ses-01_T1w.nii.gz \
                    --sid ${subjName}_ses-01 --sd /output --surfreg --fsaparc --threads 40 \
                    --parallel
    fi


    singularity run --cleanenv \
		-B ${base_dir}/bids:/bids:ro \
		-B ${base_dir}/bids/derivatives:/output_directory \
		-B ${base_dir}/micapipe_work_dir:/tmp \
		-B /data/lfs2/uqtshaw/license.txt:/opt/freesurfer-6.0.0/license.txt \
		${singularity_image} \
		-bids /bids \
		-out /output_directory \
		-sub ${subjName} \
		-ses ses-01 \
		-proc_structural \
		-post_structural \
		-MPC \
		-microstructural_img /bids/${subjName}/ses-01/anat/${subjName}_ses-01_T1map.nii.gz \
		-microstructural_reg /bids/${subjName}/ses-01/anat/${subjName}_ses-01_IV1.nii.gz \
		-proc_dwi \
		-dwi_main /bids/${subjName}/ses-01/dwi/${subjName}_ses-01_acq-b1000_dir-AP_run-1_dwi.nii.gz,/bids/${subjName}/ses-01/dwi/${subjName}_ses-01_acq-b2500_dir-AP_run-1_dwi.nii.gz \
		-dwi_rpe /bids/${subjName}/ses-01/dwi/${subjName}_ses-01_acq-b0_dir-PA_run-1_dwi.nii.gz \
		-SC \
		-tracts 20M \
		-proc_rsfmri \
		-mainScanStr rest_run_bold \
		-fmri_pe /bids/${subjName}/ses-01/func/${subjName}_ses-01_rest_run_bold.nii.gz \
		-regress_WM_CSF \
		-noFIX \
		-regAffine \
		-GD \
		-Morphology \
		-threads 40 \
		-QC_subj

done

