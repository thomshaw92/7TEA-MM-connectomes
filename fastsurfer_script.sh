#!/bin/bash

#run fastsurfer on 7TEA data
#TBS 20220917
for subjName in `cat /30days/uqtshaw/EATT/bids/subjnames.csv` ; do
    singularity_image="/data/lfs2/uqtshaw/micapipe-latest.simg"
    fastsurfer_simg="/data/lfs2/uqtshaw/fastsurfer.sif"
    base_dir="/30days/uqtshaw/EATT"
    if [[ ! -e ${base_dir}/bids/derivatives/freesurfer/${subjName}_ses-01/scripts/recon-all.done ]] ; then
	t1w=`ls /30days/uqtshaw/EATT/bids/${subjName}/ses-01/anat/${subjName}_ses-01_*_T1w.nii.gz`
	singularity exec -B ${base_dir}/bids:/data -B /30days/:/30days/ \
                    -B ${base_dir}/bids/derivatives/freesurfer/:/output \
                    -B /data/lfs2/uqtshaw/:/fs_license \
                    ${fastsurfer_simg} \
                    /fastsurfer/run_fastsurfer.sh \
                    --fs_license /fs_license/license.txt \
                    --t1 ${t1w} \
                    --sid ${subjName}_ses-01 --sd /output --surfreg --fsaparc --threads 40 \
                    --parallel
    fi

done

