# monoi_result移动到rpg/result/ 若文件不存在，则新建，并记录
import glob
import os
import shutil

import numpy as np


def copy_result(oldpath,oldname,newpath,newname,recordpath):
    oldfile = os.path.join(oldpath, oldname)
    newfile = os.path.join(newpath, newname)

    isExist = os.path.exists(oldfile)
    if not isExist:
        open(oldfile,'w') #新建txt

        record = open(recordpath,'a')
        record.write(oldfile + '\n')
        record.close()

        print('\n' + 'create null file: '+ oldname+ '.\n')
    shutil.copyfile(oldfile, newfile)

def clear_rpg(path):
    count = 0
    for root , dirs , files in os.walk(path):
        for file in glob.glob(os.path.join(root , "stamped_traj_estimate*.txt")):
            print('clear '+ file + '\n')
            os.remove(file)
            count = count +1
    print('clear rpg esti files: '+str(count)+' files has been deleted')



if __name__ == '__main__':
    out_data_path = "/home/wuhan2021/yqc/ORB_SLAM3/result_GyroWalk"
    sortd_data_path ="/home/wuhan2021/yqc/rpg_trajectory_evaluation/results/euroc_monoi/laptop"
    record_null_path = out_data_path+'/record_null_file.txt'
    a = np.arange(-1.8, 2, 0.4)           #需要修改 路径、scale（和mono文件夹数相同）
    np.set_printoptions(suppress=True)
    scale_all = 10**a
    rpg_name = ["MH_01", "MH_02", "MH_03", "MH_04", "MH_05",
                 "V1_01", "V1_02", "V1_03",
                 "V2_01", "V2_02", "V2_03"]
    output_name = []
    for i in rpg_name:
        output_name.append(i.replace("_",""))

    clear_rpg(sortd_data_path)
    count = 0
    for scale_num,scale in enumerate(scale_all):
        for round in range(0, 5):
            for file_num,file in enumerate(output_name):
                print("move: "+os.path.join('scale'+str(scale_num),'round'+str(round),file) + " to "+ 'monoi'+str(scale_num)+"/"+rpg_name[file_num] + "/traj"+str(round))
                copy_result(os.path.join(out_data_path, 'scale'+str(scale_num) , 'round'+ str(round)) ,
                            "f_dataset-"+file+"_monoi.txt",
                            os.path.join(sortd_data_path , 'monoi'+str(scale_num), 'laptop_monoi' +str(scale_num) + '_' + rpg_name[file_num]),   #scale0 对应 monoi1
                            "stamped_traj_estimate" + str(round) + ".txt",
                            record_null_path)
                count = count +1
    print(str(count)+ ' files has moved!')

