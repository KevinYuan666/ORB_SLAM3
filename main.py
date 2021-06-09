import subprocess
import os
from orbslam3_ns2s import  ns2s
import glob
import shutil

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


def copy_rmse_result(path,newpath):             #定义函数名称
    os.makedirs(newpath)
    for name in os.listdir(path):      #遍历列表下的文件名
        if name.endswith('.pdf') or name.endswith('.txt'):
             shutil.copyfile(os.path.join(path,name),os.path.join(newpath,name)) # 复制并重命名

#设置参数并修改yaml文件
def noise_para_settings(noise_scalar,para,path):  #para:需要改变的参数
    #baseline
    NoiseGyro= 1.7e-4  # 1.6968e-04
    NoiseAcc= 2.0000e-3  # 2.0e-3

    value=[]
    if para=='NoiseGyro':
        value = NoiseGyro * noise_scalar
        changeYamlConfig(path, 'IMU.NoiseGyro', value)
    elif para=='NoiseAcc':
        value = NoiseAcc * noise_scalar
        changeYamlConfig(path, 'IMU.NoiseAcc', value)

def walk_para_settings(walk_scalar, para, path):  # para:需要改变的参数
    # baseline
    GyroWalk = 1.9393e-05
    AccWalk = 3.0000e-03  # 3e-03

    value = []
    if para == 'GyroWalk':
        value = GyroWalk * walk_scalar
        changeYamlConfig(path, 'IMU.GyroWalk', value)
    elif para == 'AccWalk':
        value = AccWalk * walk_scalar
        changeYamlConfig(path, 'IMU.AccWalk', value)


def para_resume(yaml_path):
    NoiseGyro=1.7e-4  # 1.6968e-04
    NoiseAcc = 2.0000e-3  # 2.0e-3
    GyroWalk = 1.9393e-05
    AccWalk = 3.0000e-03  # 3e-03

    changeYamlConfig(yaml_path, 'IMU.NoiseGyro', NoiseGyro)
    changeYamlConfig(yaml_path, 'IMU.NoiseAcc', NoiseAcc)
    changeYamlConfig(yaml_path, 'IMU.GyroWalk', GyroWalk)
    changeYamlConfig(yaml_path, 'IMU.AccWalk', AccWalk)

def clear_rpg_results(slam_dir, rpg_data_dir):
    #claer slam
    #clear rpg
    for i, dir in enumerate(os.listdir(rpg_data_dir)):
        shutil.rmtree(rpg_data_dir+dir+'/saved_results')
        for j in glob.glob(rpg_data_dir+dir+'/stamped_traj*.txt'):
            os.remove(j)



if __name__ == '__main__':
    slam_dir=('/home/kevin/documents/evaluate_euroc/ORB_SLAM3_1/')
    rpg_dir=('/home/kevin/documents/evaluate_euroc/rpg_trajectory_evaluation_1/')

    rpg_data_dir = rpg_dir + 'results/euroc_monoi'    #用于调用rpg main

    yaml_path = slam_dir+'Examples/Monocular-Inertial/EuRoC.yaml'

    noiseScalar=[0.1, 0.2, 0.5, 1, 2, 5, 10]  #  7   4:baseline
    walkScalar =[0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10]  #10   7:baseline


    round= 10   #轨迹总个数
    para='AccWalk'
    para_type='walk'
    para_num=len(walkScalar)

    #para evaluation
    para_resume(yaml_path)

    for i in range(para_num):
        if para_type == 'walk':
            walk_para_settings(walkScalar[i], para, yaml_path)
        elif para_type == 'noise':
            noise_para_settings(noiseScalar[i], para, yaml_path)

        for j in range(round):
            subprocess.run(slam_dir + 'euroc_examples.sh')  # 运行slam
            try:
                ns2s(slam_dir, rpg_dir + 'results/euroc_monoi/AccWalk/monoi'+str(i)+'/', j)   #设置数据
            except:
                subprocess.run(slam_dir + 'euroc_examples.sh')  # 运行slam
                ns2s(slam_dir, rpg_dir + 'results/euroc_monoi/AccWalk/monoi' + str(i) + '/', j)

            for file in glob.glob(slam_dir + "*_dataset-*.txt"):   #clear slam traj result
                os.remove(file)


    # subprocess.run('python2 ' + rpg_dir + 'scripts/analyze_trajectories.py euroc_monoi.yaml --output_dir=' + rpg_data_dir + ' --results_dir=' + rpg_data_dir + ' --platform laptop --odometry_error_per_dataset --plot_trajectories --recalculate_errors --rmse_table --rmse_boxplot --overall_odometry_error --mul_trials=' + str(round), shell=True)  # 运行rpg评估   参数设置

        #转移保存结果
    #copy_rmse_result(rpg_data_dir, rpg_dir+'all_eval/'+para+'/para'+str(i+3)+'/')     #注意跑第二个参数的时候修改

        #删除RPG中的datasets
    #clear_rpg_results(slam_dir, rpg_dir + 'results/euroc_monoi/AccWalk/monoi9/')  # 注意设置路径   不需要了，因为由--recalu


        #copy_rmse_result(rpg_dir + 'results/euroc_monoi/laptop/monoi/', newpath)   有日期区别，不用复制