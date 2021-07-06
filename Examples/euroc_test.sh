#!/bin/bash
pathDatasetEuroc='../Datasets/EuRoC' #Example, it is necesary to change it by the dataset path


#------------------------------------
# Monocular-Inertial Examples


echo "Launching MH01 with Monocular-Inertial sensor"
./Monocular-Inertial/mono_inertial_euroc ../Vocabulary/ORBvoc.txt ./Monocular-Inertial/EuRoC.yaml "$pathDatasetEuroc"/MH01 ./Monocular-Inertial/EuRoC_TimeStamps/MH01.txt dataset-MH01_monoi


