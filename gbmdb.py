import csv
import hashlib
import os
import subprocess
import zipfile

from collections import defaultdict

def read_vgm_dump(dump_data):
    if type(dump_data) is bytes:
        dump_data = dump_data.decode('utf-8')
    mode = None
    position = 0
    data = defaultdict(dict)
    for line in dump_data.splitlines():
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

def read_vgm_dump_file(input_filename):
    raw_data = None
    with open(input_filename, 'r') as f:
        raw_data = f.read()
    return read_vgm_dump(raw_data)

def dump2csv(dump_data, output_filename):
    attributes = sorted(dump_data[0].keys())
    with open(output_filename, 'w') as csvfile:
        writer = csv.writer(csvfile)
        # Write headers
        writer.writerow(['smpl'] + attributes)
        for smpl in sorted(dump_data.keys()):
            line_data = [dump_data[smpl][k] for k in attributes]
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

def process_vgm_zip(input_filename, vgm2wav_path):
    print(f'processing {input_filename}')
    directory_name = input_filename.replace('.zip', '')
    with zipfile.ZipFile(input_filename) as z:
        z.extractall(directory_name)
    for filename in os.listdir(directory_name):
        if not filename.endswith('.vgz'):
            continue
        base_filename = filename.replace('.vgz', '')
        vgz_path = os.path.join(directory_name, filename)
        csv_path = os.path.join(directory_name, base_filename+'.csv')
        raw_dump_data = subprocess.check_output([vgm2wav_path, vgz_path, '/dev/null'])
        dump_data = read_vgm_dump(raw_dump_data)
        dump2csv(dump_data, csv_path)

def checksum_csvs(csv_directory):
    checksums = defaultdict(dict)
    for (dirpath, dirnames, filenames) in os.walk(csv_directory):
        for filename in filenames:
            if not filename.endswith('.csv'):
                continue
            with open(os.path.join(dirpath, filename), 'rb') as f:
                csv_data = f.read()
                sha1 = hashlib.sha1()
                sha1.update(csv_data)
                game_title = dirpath.split('/')[-1]
                checksums[game_title][filename] = sha1.hexdigest()
    return checksums