#!/bin/sh
#
#$ -S /bin/bash
#$ -v LD_LIBRARY_PATH
# 
#
#$ -l h_rt=24:00:00 
#
#
# Job name 
#$ -N FluTE-Test
#
# Use current working directory
#$ -cwd
#
# Join stdout and stderr
#$ -j y
#
# pe request for MPICH2. Set your number of processors here. 
# ORTE stands for "Open Run Time Environment".
#$ -pe orte 34
#
# Run job through bash shell
#$ -S /bin/bash
#
# The following is for reporting only. It is not really needed
# to run the job. It will show up in your output file.
echo "Got $NSLOTS processors."

#
# Use full pathname to make sure we are using the right mpirun
cd /home/dzzr/flute

time /opt/openmpi-myrinet_mx/bin/mpirun -np $NSLOTS --byslot /home/dzzr/flute/mpiflute /home/dzzr/flute/examples/config-usa


