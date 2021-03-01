import subprocess
import os
import sys
import glob
import shutil

dnull = open(os.devnull, 'w')

triage = {}

for f in glob.glob("bug-transfer/known_open/*.fe"):
    size = os.stat(f).st_size
    shutil.copy(f, "code.fe")
    with open("triage.out", 'w') as tfile:
        r = subprocess.call(["target/debug/fe code.fe"], shell=True, stdout=tfile, stderr=tfile)
    with open("triage.out", 'r') as tfile:
        for line in tfile:
            if "thread" in line:
                if "not implemented" in line:
                    break
                ms = line.split("'")
                for mc in ms:
                    if ".rs" in mc and "message" not in line:
                        m = mc
                        break
                    if "message" in mc:
                        m = "Yul compilation failed:" + mc.split('"message":')[1].split('"severity":')[0]
                        break
                if m not in triage:
                    triage[m] = (f, 1, size)
                else:
                    (ofile, count, osize) = triage[m]
                    if (size < osize):
                        triage[m] = (f, count+1, size)
                    else:
                        triage[m] = (ofile, count+1, osize)

for f in glob.glob(sys.argv[1]):
    size = os.stat(f).st_size
    shutil.copy(f, "code.fe")
    with open("triage.out", 'w') as tfile:
        r = subprocess.call(["target/debug/fe code.fe"], shell=True, stdout=tfile, stderr=tfile)
    with open("triage.out", 'r') as tfile:
        for line in tfile:
            if "thread" in line:
                if "not implemented" in line:
                    break
                ms = line.split("'")
                for mc in ms:
                    if ".rs" in mc and "message" not in line:
                        m = mc
                        break
                    if "message" in mc:
                        m = "Yul compilation failed:" + mc.split('"message":')[1].split('"severity":')[0]
                        break
                if m not in triage:
                    triage[m] = (f, 1, size)
                else:
                    (ofile, count, osize) = triage[m]
                    if (size < osize):
                        triage[m] = (f, count+1, size)
                    else:
                        triage[m] = (ofile, count+1, osize)

for t in triage:
    if "known_open" not in triage[t][0]:
        print(t, triage[t])
