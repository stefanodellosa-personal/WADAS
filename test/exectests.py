import subprocess
import sys

cmd = ["pytest"] + sys.argv[1:]
print("EXECUTING:", cmd)

process = subprocess.Popen(
    cmd, bufsize=1, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
)
for line in iter(process.stdout.readline, ""):
    print(line, end="")
    sys.stdout.flush()
process.wait()
sys.exit(process.returncode)
