import subprocess
import os
import sys
import glob
import shutil

def getMessage(mc):
    m = mc
    if "Yul" in mc:
        m = "Yul compilation failed:" + mc.split('"message":')[1].split('"severity":')[0]
    elif "analyze" in mc:
        m = "failed to analyze lowered AST:" + mc.split("message:")[1].split("labels:")[0]
        if ("No field" in m) and ("tuple_u256_bool_address" in m) and ("item000" in m):
            m = '''failed to analyze lowered AST: "No field `item00...00000` exists on struct `tuple_u256_bool_address`'''
    return m

ignoreImp = "--ignoreImp" in sys.argv
noPrune = "--noPrune" in sys.argv

dnull = open(os.devnull, 'w')

triage = {}

if not noPrune:

    for f in glob.glob("bug-transfer/known_closed/*.fe"):
        size = os.stat(f).st_size
        shutil.copy(f, "triagecode.fe")
        with open("triage.out", 'w') as tfile:
            r = subprocess.call(["ulimit -t 5; target/debug/fe triagecode.fe --overwrite --optimize"], shell=True, stdout=tfile, stderr=tfile)
        with open("triage.out", 'r') as tfile:
            for line in tfile:
                if "thread" in line:
                    if ignoreImp:
                        if "not yet implemented" in line:
                            break
                        if "not implemented" in line:
                            break
                    ms = line.split("'")
                    m = line
                    for mc in ms:
                        if ".rs" in mc and "message" not in line:
                            m = mc
                            break
                        if "message" in mc:
                            m = getMessage(mc)
                        if "ParserError: Expected 'StringLiteral' but got 'ILLEGAL'" in mc:
                            m = "ILLEGAL"
                            break
                    if "Variable name " in m and " already taken in this scope" in m:
                        m = 'Yul compilation failed:"Variable name $FOO already taken in this scope.'
                    if "Function name " in m and " already taken in this scope" in m:
                        m = 'Yul compilation failed:"Function name $FOO already taken in this scope.'
                    if m not in triage:
                        triage[m] = (f, 1, size)
                    else:
                        (ofile, count, osize) = triage[m]
                        if (size < osize):
                            triage[m] = (f, count+1, size)
                        else:
                            triage[m] = (ofile, count+1, osize)

    for f in glob.glob("bug-transfer/known_open/*.fe"):
        size = os.stat(f).st_size
        shutil.copy(f, "triagecode.fe")
        with open("triage.out", 'w') as tfile:
            r = subprocess.call(["ulimit -t 5; target/debug/fe triagecode.fe --overwrite --optimize"], shell=True, stdout=tfile, stderr=tfile)
        with open("triage.out", 'r') as tfile:
            for line in tfile:
                if "thread" in line:
                    if ignoreImp:
                        if "not implemented" in line:
                            break
                        if "not yet implemented" in line:
                            break                
                    ms = line.split("'")
                    m = line
                    for mc in ms:
                        if ".rs" in mc and "message" not in line:
                            m = mc
                            break
                        if "message" in mc:
                            m = getMessage(mc)
                        if "ParserError: Expected 'StringLiteral' but got 'ILLEGAL'" in mc:
                            m = "ILLEGAL"
                            break
                    if "Variable name " in m and " already taken in this scope" in m:
                        m = 'Yul compilation failed:"Variable name $FOO already taken in this scope.'
                    if "Function name " in m and " already taken in this scope" in m:
                        m = 'Yul compilation failed:"Function name $FOO already taken in this scope.'
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
    shutil.copy(f, "triagecode.fe")
    with open("triage.out", 'w') as tfile:
        r = subprocess.call(["ulimit -t 5; target/debug/fe triagecode.fe --overwrite --optimize"], shell=True, stdout=tfile, stderr=tfile)
    with open("triage.out", 'r') as tfile:
        for line in tfile:
            if "thread" in line:
                if not noPrune:
                    if "not implemented" in line:
                        break
                    if "not yet implemented" in line:
                        break
                ms = line.split("'")
                m = line
                for mc in ms:
                    if ".rs" in mc and "message" not in line:
                        m = mc
                        break
                    if "message" in mc:
                        m = getMessage(mc)
                    if "ParserError: Expected 'StringLiteral' but got 'ILLEGAL'" in mc:
                        m = "ILLEGAL"
                        break
                if "Variable name " in m and " already taken in this scope" in m:
                    m = 'Yul compilation failed:"Variable name $FOO already taken in this scope.'
                if "Function name " in m and " already taken in this scope" in m:
                    m = 'Yul compilation failed:"Function name $FOO already taken in this scope.'
                if m not in triage:
                    triage[m] = (f, 1, size)
                else:
                    (ofile, count, osize) = triage[m]
                    if (size < osize) and ("known" not in ofile):
                        triage[m] = (f, count+1, size)
                    else:
                        triage[m] = (ofile, count+1, osize)

for t in triage:
    if "Bad escape sequence" in t: # Needs special casing to ignore
        continue
    if noPrune:
        print(t, triage[t][:-2])
        continue
    if "known_closed" in triage[t][0]:
        print("KNOWN CLOSED:", triage[t][:-2])
    elif "known_open" in triage[t][0]:
        if triage[t][1] > 1:
            print("KNOWN OPEN:", triage[t][:-2])
    else:
        print(t, triage[t][:-2])
