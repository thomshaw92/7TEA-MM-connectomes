#!/bin/bash

#run micapipe on 7TEA data
#TBS 20220917
for subjName in sub-080 sub-090 sub-100 sub-110 sub-120 ; do
    singularity_image="/data/lfs2/uqtshaw/micapipe-latest.simg"
    fastsurfer_simg="/data/lfs2/uqtshaw/fastsurfer.sif"
    base_dir="/90days/uqtshaw/USyd_UQ_dwi_examples"
   if [[ ! -e ${base_dir}/bids/derivatives/freesurfer/${subjName}_ses-01/scripts/recon-all.done ]] ; then
	singularity exec -B ${base_dir}/bids:/data \
                    -B ${base_dir}/bids/derivatives/freesurfer/:/output \
                    -B /data/lfs2/uqtshaw/:/fs_license \
                    ${fastsurfer_simg} \
                    /fastsurfer/run_fastsurfer.sh \
                    --fs_license /fs_license/license.txt \
                    --t1 /data/${subjName}/anat/${subjName}_T1w.nii.gz \
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
		-proc_dwi \
		-dwi_main /bids/${subjName}/ses-01/dwi/${subjName}_dir-AP_dwi.nii.gz \
		-dwi_rpe /bids/${subjName}/ses-01/dwi/${subjName}_dir-PA_dwi.nii.gz \
		-SC \
		-regAffine \
		-GD \
		-Morphology \
		-threads 40 \
		-QC_subj

done
