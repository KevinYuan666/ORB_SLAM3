import subprocess
import os
import glob
import shutil
import math
import numpy as np


#yaml文件处理
def changeYamlConfig(path, key, value):
    with open(path, 'r', encoding='utf-8') as f:
        lines = []  # 创建了一个空列表，里面没有元素
        for line in f.readlines():
            if line != '\n':
                lines.append(line)
        f.close()
    with open(path, 'w', encoding='utf-8') as f:
        flag = 0
        for line in lines:
            if key in line:
                leftstr = line.split(":")[0]
                newline = "{0}: {1}".format(leftstr, value)
                line = newline
                f.write('%s\n' % line)
                flag = 1
            else:
                f.write('%s' % line)
        f.close()
        return flag


def copy_rmse_result(oldpath,newpath):             #定义函数名称
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    for file in glob.glob(oldpath + "/f_dataset-*.txt"):
        shutil.copyfile(os.path.join(oldpath, file), os.path.join(newpath, file.replace(oldpath+'/','')))  # 复制数据并重命名
        os.remove(os.path.join(oldpath, file))

# noise walk分别设置的函数
def noise_para_settings(noise_scalar,para,yaml_path):  #para:需要改变的参数
    #baseline
    NoiseGyro= 1.7e-4  # 1.6968e-04
    NoiseAcc= 2.0000e-3  # 2.0e-3

    value=[]
    if para=='NoiseGyro':
        value = NoiseGyro * noise_scalar
        changeYamlConfig(yaml_path, 'IMU.NoiseGyro', value)
    elif para=='NoiseAcc':
        value = NoiseAcc * noise_scalar
        changeYamlConfig(yaml_path, 'IMU.NoiseAcc', value)

def walk_para_settings(walk_scalar, para, yaml_path):  # para:需要改变的参数
    # baseline
    GyroWalk = 1.9393e-05
    AccWalk = 3.0000e-03  # 3e-03

    value = []
    if para == 'GyroWalk':
        value = GyroWalk * walk_scalar
        changeYamlConfig(yaml_path, 'IMU.GyroWalk', value)
    elif para == 'AccWalk':
        value = AccWalk * walk_scalar
        changeYamlConfig(yaml_path, 'IMU.AccWalk', value)

#同时改变4个参数
def all_para_settings(scale , yaml_path):
    NoiseGyro=1.7e-4  # 1.6968e-04
    NoiseAcc = 2.0000e-3  # 2.0e-3
    GyroWalk = 1.9393e-05
    AccWalk = 3.0000e-03  # 3e-03

    changeYamlConfig(yaml_path, 'IMU.NoiseGyro', NoiseGyro * scale)
    changeYamlConfig(yaml_path, 'IMU.NoiseAcc', NoiseAcc * scale)
    changeYamlConfig(yaml_path, 'IMU.GyroWalk', GyroWalk * scale)
    changeYamlConfig(yaml_path, 'IMU.AccWalk', AccWalk * scale)

def para_resume(yaml_path):
    NoiseGyro=1.7e-4  # 1.6968e-04
    NoiseAcc = 2.0000e-3  # 2.0e-3
    GyroWalk = 1.9393e-05
    AccWalk = 3.0000e-03  # 3e-03

    changeYamlConfig(yaml_path, 'IMU.NoiseGyro', NoiseGyro)
    changeYamlConfig(yaml_path, 'IMU.NoiseAcc', NoiseAcc)
    changeYamlConfig(yaml_path, 'IMU.GyroWalk', GyroWalk)
    changeYamlConfig(yaml_path, 'IMU.AccWalk', AccWalk)



if __name__ == '__main__':
    #目标：IMU噪声参数四个参数同时调，scale : 10^-3 to 10^3 每种跑10次

    slam_dir='/home/wuhan2020/yqc/ORB_SLAM3'
    save_dir= '/home/wuhan2020/yqc/ORB_SLAM3/monoi_result'
    yaml_path = slam_dir+'/Examples/Monocular-Inertial/EuRoC.yaml'
    #生成噪声参数scale
    a = np.arange(-1, 1.2, 0.2)
    np.set_printoptions(suppress=True)
    scale_all = 10**a

    for num,scale in enumerate(scale_all):
        all_para_settings(scale, yaml_path)
        for round in range(0,5):  #跑10次重复
            subprocess.run(slam_dir + '/Examples/euroc_test.sh')  # 运行slam
            copy_rmse_result(slam_dir+ '/Examples', os.path.join(save_dir,'scale'+str(num),'round' + str(round)))  # 注意跑第二个参数的时候修改


    # subprocess.run('python2 ' + rpg_dir + 'scripts/analyze_trajectories.py euroc_monoi.yaml --output_dir=' + rpg_data_dir + ' --results_dir=' + rpg_data_dir + ' --platform laptop --odometry_error_per_dataset --plot_trajectories --recalculate_errors --rmse_table --rmse_boxplot --overall_odometry_error --mul_trials=' + str(round), shell=True)  # 运行rpg评估   参数设置

        #转移保存结果
    # copy_rmse_result(rpg_data_dir, rpg_dir+'all_eval/'+para+'/para'+str(i+3)+'/')     #注意跑第二个参数的时候修改

        #删除RPG中的datasets
    #clear_rpg_results(slam_dir, rpg_dir + 'results/euroc_monoi/AccWalk/monoi9/')  # 注意设置路径   不需要了，因为由--recalu


        #copy_rmse_result(rpg_dir + 'results/euroc_monoi/laptop/monoi/', newpath)   有日期区别，不用复制