toolkits:
STEP 1:
run_orbslam3.py		generate the orbslam3 datasets

STEP 2:
move_orbslam3 datasets to monoi 

STEP 3:
generate_origin_algorithm_dir.py    generate different algorithm original dirs which has the same groundtruth and config in rpg directory   problems: subfolders should be renamed after it.

STEP 4:
move2rpg.py	move the monoi_results to the corresponding directory(scale, round, dataset(MH01-V203))  why:each round and scale output files of orbslam3 should be transfer to another folder beacuse the next round will cover them. 

STEP 5:
orbslam3_ns2s.py	modify the first column unit ns to s (divide 10^9(1e9))  why: orbslam3(ns) output data unit isn't identical to rpg evaluation(s). use: it can be used to main floder, like 'rpg/results/monoi/laptop', to modify time units of all files in the same name type in the subfloders. 


refine: 1, no need of step 2, move to rpg directly. problem: the orbslam3 will fail. you should create a new null file and record it. 
	2, by modify the orbslam3 output, step 5 can be delete.



