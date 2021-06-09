# ORBSALM3中的estimate文件转换格式并导入到results
# 循环进入每文件夹，将stamped_traj_estimate.txt中的time单位由ns 到 s
import os

#读取估计轨迹文件并更改数据
def ns2s(old_dir, new_dir, num):


    #读取旧数据放进新的里
    for i,dir in  enumerate(os.listdir(new_dir)):
        new_all_line = []
        old_all_line = []
        new_path=(new_dir + dir + '/stamped_traj_estimate'+str(num)+'.txt')  #新文件名
        match_name=dir[-5:-3]+dir[-2:]  #截取后面的字符用于匹配新旧文件
        old_path = old_dir + 'f_dataset-'+match_name+'_monoi.txt'

        #读旧的
        with open(old_path,'r') as f:
        #获取需要估计文件的每一行
            for line in f:
                sp_line=line.split()
                sp_line[0]=str(float(sp_line[0])/10e8)
                new_line=(' '.join(sp_line)+'\n')
                old_all_line.append(line)
                new_all_line.append(new_line)

        with open(new_path,'a') as w:
            for w_line_index,w_line in enumerate(new_all_line):
                w.write(w_line)
        f.close()
        w.close()
