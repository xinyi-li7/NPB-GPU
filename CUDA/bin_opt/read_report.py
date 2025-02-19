import subprocess
import os
import pandas as pd
import glob

def setup_module(module):
    THIS_DIR = os.path.dirname(os.path.abspath(__file__))
    os.chdir(THIS_DIR)

def teardown_module(module):
    cmd = ["make clean"]
    cmdOutput = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)

def run_command(cmd):
    try:
        cmdOutput = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as e:
        print(e.output)
        exit()
    return cmdOutput

from contextlib import contextmanager
import os

@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)
    
def read_report(report, data_list):
    assert(len(report) >= 10)
    for line in report:
        #print(line)
        if("NaN found" in line or "INF found" in line):
            line_set = line.split("              ")
        elif("underflow (subnormal)" in line):
            line_set = line.split("  ")
        elif("Total Division by 0" in line):
            line_set = line.split("          ")
        elif("Kernels" in line):
            line_set = line.split("      ")
        elif("FP Inst. count" in line):
            line_set = line.split("  ")
        else:
            line_set = []
        #print(line_set)
        if(len(line_set)==2):
            num = line_set[1].split("\n")[0]
            data_list.append(num)
    #print(report)
    assert(len(data_list) == 11)
    return data_list

def to_time_s(t):
    time_list = t.split('m')
    return float(time_list[0])*60+float(time_list[1].split('s')[0])

def time_info(infos):
    count = 0
    for line in infos:
        count = count +1
        if("real" in line):
            assert("user" in infos[count])
            assert("sys" in infos[count+1])
            t = line.split("	")[1]
            t_s = to_time_s(t)
    return t_s

           

# dirs=["mum", "mri-q", "libor", "cutcp", "nbody", "BlackScholes", "backprop", "tpacf", "srad", "fdtd3d", "gaussian", "particlefilter", "reduction", "MonteCarlo", "kmeans", "wp", "scalarProd", "dct8x8", "mersenne", "sgemm", "oceanFFT", "lud", "rayTracing", "cfd", "dwthaar", "particles", "gramschm", "alirt", "mri-gridding", "md", "spmv", "corr", "hotspot", "cp", "myocyte", "recursiveGaussian", "SobolQRNG", "nn", "binomial", "eigenvalues", "transpose", "lps", "sp", "bh", "lineOfSight"]
# dirs=["mum", "cfd"]
# dirs=["alirt", "backprop", "bh", "binomial", "BlackScholes", "cfd", "corr", "cp", "cutcp", "dct8x8", "dwthaar", "eigenvalues", "fdtd3d", 
# "fft", "gaussian", "gramschm", "heartwall", "hotspot", "kmeans", "libor", "lineOfSight", "lps", "lud", "md",
#  "mersenne", "MonteCarlo", "mri-gridding", "mri-q", "mum", "myocyte", "nbody", "nn", "oceanFFT", "particlefilter", 
#  "particles", "rayTracing", "recursiveGaussian", "reduction", "s3d", "scalarProd", "sgemm", "single", "SobolQRNG", "sp", "spmv", "srad", "stencil", "tpacf","transpose","wp"]

#df = pd.DataFrame(columns = ["program","fp64_NAN", "fp64_INF", "fp64_SUB","fp64_DIV0","fp32_NAN", "fp32_INF", "fp32_SUB","fp32_DIV0","kernel","FP instructions","check_time","ori_time","slowdown"])
df = pd.DataFrame(columns = ["program","fp64_NAN", "fp64_INF", "fp64_SUB","fp64_DIV0","fp32_NAN", "fp32_INF", "fp32_SUB","fp32_DIV0","kernel","FP instructions","check_time"])
def create_table(dirs):
    for dir in dirs:
        print("process application: ", dir)
        with cd(dir):
        # run_command(["cd ",dir])
        # print(run_command([comd]))
            # for x in glob.glob("./*"):
            #     print(x)
            with open("stdout.txt") as f:
                exist = 0
                lines_list = f.readlines()
                count = 0
                for line in lines_list:
                    # print(line)
                    count = count + 1
                    if("FPChecker Report" in line):
                        exist = 1
                        e = read_report(lines_list[count+1:],[dir])
                        break
            # print("exist is: ", exist)
            if(exist != 0):
                with open("stderr.txt") as time_f:
                    infos = time_f.readlines()
                    t_s = time_info(infos)
                    e.append(t_s)
#                with open("stderr_ori.txt") as timeori_f:
#                    infos_ori = timeori_f.readlines()
#                    t_s_ori = time_info(infos_ori)
#                    e.append(t_s_ori)   
#                slowdown = t_s/t_s_ori
#                e.append(slowdown)
                df.loc[len(df)] = e
            else:
                e = [dir,"N/A", "N/A", "N/A", "N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A"]
                df.loc[len(df)] = e
            cd("..")

    print(df)
    df.to_csv("parse_report.csv", index=False)
                #raise Exception("cannot go back to last directory")

def entry(start_dir):
    dir_list = []
    for f in glob.iglob(start_dir+'/**/stdout.txt',recursive=True):
        d = '/'.join(f.split('/')[:-1])
        dir_list.append(d)
    create_table(dir_list)    
        

if __name__ == "__main__":
    entry("./")
