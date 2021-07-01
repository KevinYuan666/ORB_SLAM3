# 循环进入每文件夹，time单位由ns 到 s
import os
import glob

# 将子目录下所有TXT文件 时间单位全部修改
def ns2s(file):

    new_all_line = []
    old_all_line = []
    #读旧的
    with open(file,'r') as f:
    #获取需要估计文件的每一行
        for line in f:
            sp_line=line.split()
            sp_line[0]=str(float(sp_line[0])/1e9)
            new_line=(' '.join(sp_line)+'\n')
            old_all_line.append(line)
            new_all_line.append(new_line)
    f.close()
    with open(file,'w') as w:
        for w_line_index,w_line in enumerate(new_all_line):
            w.write(w_line)
    w.close()

if __name__ == '__main__':
    path = "/home/wuhan2020/yqc/rpg_trajectory_evaluation/results/euroc_monoi/laptop"
    filetype = "stamped_traj_estimate*.txt"

    #找到目录下，包括子目录所有以 filetype 命名的文件， 并依次修改
    count = 0
    for root , dirs , files in os.walk(path):
        print('\n'+root)
        for name in glob.glob(os.path.join(root , filetype)):
            print('modify '+name.replace(path,''))
            count = count +1
            ns2s(name)
    print(str(count) + ' files have been modified')