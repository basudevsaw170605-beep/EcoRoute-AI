import os
for root, dirs, files in os.walk(r'D:\Project\EcoRoute-AI\src'):
    for f in files:
        if f.endswith('.py'):
            path = os.path.join(root, f)
            with open(path) as fh:
                for i, line in enumerate(fh, 1):
                    if '.split(' in line:
                        print(f'{path}:{i}: {line.rstrip()}')