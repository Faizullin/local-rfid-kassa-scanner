import os, subprocess, sys

cmd = []
if os.name == 'nt':
    cmd.append('py')
else:
    cmd.append('python3')

args = sys.argv[1:]

if '--train' in args or '-t' in args:
    cmd.append('train_face.py')
elif '--migrate' in args or '-m' in args:
    cmd.append('./src/enter_col.py')
    cmd += args
else:
    cmd.append('main.py')
print(cmd)
subprocess.run(cmd)
