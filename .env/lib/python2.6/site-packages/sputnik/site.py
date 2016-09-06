import os
import csv


def add_path(mod_name, path):
    record_path = get_record_path(mod_name)
    if record_path:
        full_path = '/'.join([mod_name, path])
        if not record_has_path(record_path, full_path):
            record_add_path(record_path, full_path)


def get_mod_path(mod_name):
    try:
        mod = __import__(mod_name, globals(), locals(), 0)
    except ImportError:
        return
    return os.path.join(os.path.dirname(mod.__file__))


def get_meta_path(mod_name):
    mod_path = get_mod_path(mod_name)
    if not mod_path:
        return
    path = os.path.join(mod_path, '..')
    for item in os.listdir(path):
        if item.startswith(mod_name) and item.endswith('dist-info'):
            return os.path.join(path, item)


def get_record_path(mod_name):
    meta_path = get_meta_path(mod_name)
    if not meta_path:
        return
    record_path = os.path.abspath(os.path.join(meta_path, 'RECORD'))
    if os.path.exists(record_path):
        return record_path


def record_has_path(record_path, path):
    with open(record_path) as f:
        for row in csv.reader(f):
            if row[0] == path:
                return True
    return False


def record_add_path(record_path, path):
    with open(record_path, 'a') as f:
        csvfile = csv.writer(f)
        csvfile.writerow([path, None, None])
