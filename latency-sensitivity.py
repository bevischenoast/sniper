#!/bin/python
import os

soplex = "SPEC06/binaries/soplex -s1 -e -m45000 SPEC06/data/soplex/ref/input/pds-50.mps"
leslie3d = "SPEC06/binaries/leslie3d SPEC06/data/leslie3d/ref/input/leslie3d.in"
lbm = "SPEC06/binaries/lbm 3000 SPEC06/data/lbm/ref/output/reference.dat 0 0 SPEC06/data/lbm/ref/input/100_100_130_ldc.of"
astar = "SPEC06/binaries/astar BigLakes2048.cfg"
GemsFDTD = "SPEC06/binaries/GemsFDTD"
milc = "SPEC06/binaries/milc < SPEC06/data/milc/ref/input/su3imp.in"
mcf = "SPEC06/binaries/mcf SPEC06/data/mcf/ref/input/inp.in"
gcc = "SPEC06/binaries/gcc SPEC06/data/gcc/ref/input/166.in -o SPEC06/data/gcc/ref/output/166.s"
cactusADM = "SPEC06/binaries/cactusADM SPEC06/data/cactusADM/ref/input/benchADM.par"
zeusmp = "SPEC06/binaries/zeusmp"
bzip2 = "SPEC06/binaries/bzip2 SPEC06/data/bzip2/ref/input/input.source 280"
h264ref = "SPEC06/binaries/h264ref -d SPEC06/data/h264ref/ref/input/foreman_ref_encoder_baseline.cfg"
xalancbmk = "SPEC06/binaries/xalancbmk -v SPEC06/data/xalancbmk/ref/input/t5.xml SPEC06/data/xalancbmk/ref/input/xalanc.xsl"

libquantum = "SPEC06/binaries/libquantum 1397 8"
omnetpp = "SPEC06/binaries/omnetpp omnetpp.ini"
bwaves = "SPEC06/binaries/bwaves"
dealII = "SPEC06/binaries/dealII 23"

mix1 = "benchmarks="+bzip2+", "+libquantum+", "+astar+", "+cactusADM
mix2 = "benchmarks="+lbm+", "+omnetpp+", "+mcf+", "+GemsFDTD
mix3 = "benchmarks="+h264ref+", "+milc+", "+bwaves+", "+gcc
mix4 = "benchmarks="+soplex+", "+astar+", "+soplex+", "+zeusmp
mix5 = "benchmarks="+bzip2+", "+mcf+", "+dealII+", "+gcc
mix6 = "benchmarks="+omnetpp+", "+bwaves+", "+GemsFDTD+", "+cactusADM
mix7 = "benchmarks="+leslie3d+", "+xalancbmk+", "+h264ref+", "+astar
mix8 = "benchmarks="+soplex+", "+dealII+", "+GemsFDTD+", "+cactusADM
mix9 = "benchmarks="+lbm+", "+soplex+", "+leslie3d+", "+h264ref

benchmarks = [soplex, leslie3d, lbm, astar, GemsFDTD, milc, mcf, gcc,
              cactusADM, zeusmp, bzip2, h264ref, xalancbmk]

benchmark_names = ["soplex", "leslie3d", "lbm", "astar", "GemsFDTD", "milc", "mcf", "gcc",
                   "cactusADM", "zeusmp", "bzip2", "h264ref", "xalancbmk"]

latencys = ["20", "30", "40", "50", "60"]

for benchmark_name, benchmark in zip(benchmark_names, benchmarks):
    for latency in latencys:
        cmdline = "./run-sniper -n 4 -d ./result/" + benchmark_name + "/" + latency + "/ -c gainestown -s roi-icount:10000000000:0:1000000000 --roi-script -g --perf_model/l3_cache/data_access_time=" + latency + " -- " + benchmark + " & "
        os.system(cmdline)
        #print(cmdline)



