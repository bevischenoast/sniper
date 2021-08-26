#!/bin/python
import os

target_file = open("lat_sensitivity.xls", "w")

benchmarks = ["soplex", "leslie3d", "lbm", "astar", "GemsFDTD", "milc", "mcf", "gcc",
              "cactusADM", "zeusmp", "bzip2", "h264ref", "xalancbmk", "mix1", "mix2", "mix3", "mix4", "mix5",
              "mix6", "mix7", "mix8", "mix9"]

latencys = ["20", "30", "40", "50", "60"]

keyword = "IPC"

for latency in latencys:
    target_file.write("\t" + format(latency, '>20'))
target_file.write("\n")

for benchmark in benchmarks:
    message = benchmark
    for latency in latencys:
        source_file_dir = "result/" + benchmark + "/" + latency + "/sim.out"
        source_file = open("source_file_dir", "r")
        lines = source_file.readlines()
        for line in lines:
            if keyword in lines:
                line = line.rstrip('\n')
                elements = keyword.split(": ")
                message = message + "\t" + elements[1]
    target_file.write(message + "\n")

print("---> Result was saved in result.xls")
