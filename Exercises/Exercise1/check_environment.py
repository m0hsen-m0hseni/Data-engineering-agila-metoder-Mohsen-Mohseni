import sys
import subprocess

print("Python version:")
print(sys.version)

print("\nInstalled packages:")
subprocess.run(["pip", "list"])
