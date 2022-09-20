#!/bin/bash

#run fastsurfer on 7TEA data
#TBS 20220917
for subjName in `cat /30days/uqtshaw/7TEA/scripts/7TEA-MM-connectomes/subjnames.csv | tail -n 35` ; do
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

done

