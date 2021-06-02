import sys

def take_data(args):
    for arg in args:
        if arg.split('=')[0] == 'op':
            continue
            
        name = arg.split('=')[0]
        variables[name] = float(arg.split('=')[1])

stdin_lines = []
variables = {}
result = 0

print("Recibido por STDIN: ")
try:
    for line in sys.stdin:
        print(line)
        stdin_lines.append(line)
except:
    print('Error STDIN')
print()
print()

i = 0
for line in stdin_lines:
    args = line.split('&')
    operation = args[0].split('=')[1]
    if operation == 'sum':
        take_data(args)
        for value in variables.values():
            if i == 0:
                result = value
                i+=1
                continue
            result += value
    elif operation == 'sub':
        take_data(args)
        for value in variables.values():
            if i == 0:
                result = value
                i+=1
                continue
            result -= value
    elif operation == 'mul':
        take_data(args)
        for value in variables.values():
            if result == 0:
                result = value
                continue
            result *= value
    elif operation == 'div':
        take_data(args)
        for value in variables.values():
            if result == 0:
                result = value
                continue
            result /= value

    print('Variables', variables)
    print('Operacion', operation)
    print('Resultado', result)
