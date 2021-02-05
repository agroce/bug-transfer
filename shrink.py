import subprocess
import os
import shutil
import sys

charShrink = "--chars" in sys.argv

def bug():
    with open("triage.out", 'w') as tfile:
        r = subprocess.call(["target/debug/fe code.fe"], shell=True, stdout=tfile, stderr=tfile)
    m = None
    with open("triage.out", 'r') as tfile:
        for line in tfile:
            if "thread" in line:
                ms = line.split("'")
                for mc in ms:
                    if ".rs" in mc and "message" not in line:
                        m = mc
                        break
                    if "message" in mc:
                        m = "Yul compilation failed:" + mc.split('"message":')[1].split('"severity":')[0]
                        break
    return m

dnull = open(os.devnull, 'w')

code = []

with open("start.fe", 'r') as f:
    code = f.readlines()

shutil.copy("start.fe", "code.fe")
initial_bug = bug()
    
changed = True
while changed:
    changed = False
    for pos in range(len(code)):
        for stride in range(1,3):
            with open("code.fe", 'w') as f:
                i = 0
                omitted = range(pos,pos+stride)
                for line in code:
                    if i not in omitted:
                        f.write(line)
                    i += 1
            new_bug = bug()
            if new_bug == initial_bug:
                print("REMOVING LINE", pos, "STRIDE", stride, "WORKED:")
                print("NEW LENGTH:", len(code)-1)
                changed = True
                newcode = code[:pos] + code[pos+stride:]
                code = newcode
                with open("finish.fe", 'w') as f:
                    for line in code:
                        f.write(line)
                break
        if changed:
            break

if not charShrink:
    sys.exit(0)
        
code = "".join(code)
        
changed = True
while changed:
    changed = False
    for pos in range(len(code)):
        for stride in range(1,3):
            with open("code.fe", 'w') as f:
                i = 0
                omitted = range(pos,pos+stride)
                for line in code:
                    if i not in omitted:
                        f.write(line)
                    i += 1
            new_bug = bug()
            if new_bug == initial_bug:
                print("REMOVING CHAR", pos, "STRIDE", stride, "WORKED:")
                print("NEW LENGTH:", len(code)-1)
                changed = True
                newcode = code[:pos] + code[pos+stride:]
                code = newcode
                with open("finish.fe", 'w') as f:
                    for line in code:
                        f.write(line)
                break
        if changed:
            break
