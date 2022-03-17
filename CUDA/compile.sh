APPs='BT CG EP FT IS LU MG SP'
Classes='S W A B C'
for class in $Classes
do
    for app in $APPs
    do
        make $app CLASS=$class
    done
done