import csv
from collections import defaultdict

def read_vgm_dump(input_filename):
    raw_data = None
    with open(input_filename, 'r') as f:
        raw_data = f.read()
    mode = None
    position = 0
    data = defaultdict(dict)
    for line in raw_data.splitlines():
        if line.startswith('mode:'):
            mode = line.split()[-1]
            continue
        if line.startswith('VGMSmplPos'):
            position = int(line.split()[-1])
            continue
        key, value = line.split()
        value = int(value)
        data[position][mode + '_' + key] = value
    return data

def dump2csv(input_filename, output_filename):
    data = read_vgm_dump(input_filename)
    attributes = sorted(data[0].keys())
    with open(output_filename, 'w') as csvfile:
        writer = csv.writer(csvfile)
        # Write headers
        writer.writerow(['smpl'] + attributes)
        for smpl in sorted(data.keys()):
            line_data = [data[smpl][k] for k in attributes]
            writer.writerow([smpl] + line_data)

def csv2dump(input_filename):
    data = defaultdict(dict)
    with open(input_filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for i, row in enumerate(reader):
            if i == 0:
                headers = row
                continue
            smpl = int(row[0])
            data[smpl] = {headers[ci]: int(ce) for ci, ce in enumerate(row)}
    return data