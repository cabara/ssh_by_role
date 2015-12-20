#! /usr/bin/python3

import argparse
import os
import subprocess
import json

parser = argparse.ArgumentParser()
parser.add_argument('word')
parser.add_argument('--no-ssh', action='store_true')
args = parser.parse_args()

home_path = os.environ['HOME']
inventory_script = os.path.join(home_path, '.scripts/ssh_by_role/inventory.py')
run_inventory = subprocess.Popen([inventory_script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
string_inventory, error= run_inventory.communicate('S\nL\n')
inventory = json.loads(string_inventory.decode('utf-8'))

roles = list(filter(lambda role: args.word in role, inventory.keys()))
print('\n'.join(
    [
        "%s: --> %s" % (number, role)
        for number, role in
        zip(
            range(len(roles)),
            roles 
        )
    ]
))
print('enter number of role (defualt 0):')
index = input()
index = int(index) if index else 0

role = roles[index]

hosts = inventory[role].get('hosts')
host = hosts[0]

if not args.no_ssh:
    os.system('ssh -i ~/.ssh/keypair.pem ubuntu@%s' % host)

