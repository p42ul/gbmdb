from collections import defaultdict

def read_dump(filename, target_mode):
    raw_data = None
    with open(filename, 'r') as f:
        raw_data = f.read()
    mode = None
    position = 0
    ret = defaultdict(dict)
    for line in raw_data.splitlines():
        if line.startswith('mode:'):
            mode = line.split()[-1]
            continue
        if line.startswith('VGMSmplPos'):
            position = int(line.split()[-1])
            continue
        if mode != target_mode:
            continue
        key, value = line.split()
        value = int(value)
        ret[position][key] = value
    return ret