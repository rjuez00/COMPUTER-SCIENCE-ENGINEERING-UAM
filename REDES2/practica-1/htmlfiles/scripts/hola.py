import sys
from time import sleep
stdin_lines = []

print("Recibido por STDIN: ")
try:
    for line in sys.stdin:
        print(line)
        stdin_lines.append(line)
except:
    print('Error STDIN')
print()
print()
sleep(10)

variables = {}

for line in stdin_lines:
    args = line.split('&')
    for arg in args:
        nombre = arg.split('=')[0]
        variables[nombre] = arg.split('=')[1]
        print('Hola '+variables[nombre]+'!')

print('Variables', variables)