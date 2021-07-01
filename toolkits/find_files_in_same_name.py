from move2rpg import copy_result
import glob,os

if __name__ == '__main__':
    path = '/home/wuhan2020/yqc/test_file'
    count = 0
    for root , dirs , files in os.walk(path):
        print('\n'+root)
        for name in glob.glob(os.path.join(root , "stamped_traj_estimate*.txt")):
            print(name)
            count = count +1
    print(count)