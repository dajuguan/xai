import os
import sys
import subprocess
import time
from subprocess import Popen, PIPE, STDOUT
import json
with open(".env") as f:
    operator = json.load(f)
prv_key = operator["prv_key"]+"\n"


proc = subprocess.Popen("./sentry-node-cli-linux", stdin=PIPE, text=True)

#------------------some test---------------------------#
# proc.stdin.write('list-operators\n')
# proc.stdin.flush()
# proc.stdin.write('0xcAaC5C5a967454807A0B83F408f19AD6542d7b51\n')
# proc.stdin.flush()
# time.sleep(0.5)

# -----------------boot-opearator-------------------------#
proc.stdin.write('boot-operator\n')
proc.stdin.write(prv_key)
proc.stdin.flush()
time.sleep(0.5)
# -----------------priovison------------------------------#
proc.stdin.write('y\n')
proc.stdin.flush()
time.sleep(0.5)
proc.stdin.write(' \n\n')
proc.stdin.flush()
proc.wait()
