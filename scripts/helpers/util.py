
import json
import importlib.util
import subprocess
import datetime

def read_JSON(filename):
    """Reads json file of the given name, parses it and returns the dictionary object"""
    with open(filename, 'r') as f:
        data=f.read()
    return json.loads(data)

def write_JSON(dictionary, filename):
    with open(filename, 'w+') as f:
        f.write(to_JSON(dictionary))
    return

def to_JSON(dictionary):
    return json.dumps(dictionary, indent=4)

def import_script_from_filename(filename):
    spec = importlib.util.spec_from_file_location("module.name", filename)
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    return foo

def execute_sys_command(args, stdout):
    """Executes the given system-level command"""
    return subprocess.Popen(args, stdout=stdout, shell=True)

def echo(msg):
    print ("### USER LOG #### {0}".format(msg))