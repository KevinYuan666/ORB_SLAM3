import os
import shutil

if __name__ == '__main__':
    path = "/home/wuhan2020/yqc/rpg_trajectory_evaluation/results/euroc_monoi/laptop"
    for algo in range(1,8):
        shutil.copytree(os.path.join(path, "monoi"), os.path.join(path, "monoi"+str(algo)))