Classes='S W A B C'
#Classes='S'
export FP_EXCEPTION_HOME=/home/xinyi/nvbit_release/tools/detect_fp_exceptions
export PRELOAD_FLAG="LD_PRELOAD=${FP_EXCEPTION_HOME}/detect_fp_exceptions.so"
for c in $Classes
do
    exes=$(find ./ -name "*.$c")
    for exe in $exes 
    do
        tail=${exe##*.}
        size=${#tail}
        app=${exe::(-$size-1)}
        dir="${app}_${tail}"
        rm -rf ${dir}
        mkdir $dir
        echo "eval ${PRELOAD_FLAG} ../${exe}" > ${dir}/tmp.sh
        cd ${dir}
        curDir=$(pwd)
        echo "in direcoty ${curDir}"
        (time timelimit -t1200 bash tmp.sh) >stdout.txt 2>stderr.txt
        cd ..
    done
done