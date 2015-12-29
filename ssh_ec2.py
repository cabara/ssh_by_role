#! /usr/bin/python3

import argparse
import os
import subprocess
import json

def print_with_indexes(items):
    print('\n'.join(
        [
            "%s: --> %s" % (number, item)
            for number, item in
            zip(
                range(len(items)),
                items
            )
        ]
    ))

home_path = os.environ['HOME']
inventory_script = os.path.join(home_path, '.scripts/ssh_ec2.py/inventory.py')

parser = argparse.ArgumentParser()
parser.add_argument('search_tag', help="string with which EC2 host will be looked with")

parser.add_argument('--no-ssh', action='store_true', help="won't ssh just print out the host dns")
parser.add_argument('--tag', default="role", help="what EC2 tag to search")
parser.add_argument('--ssh-key', default="~/.ssh/keypair.pem", help="path to the ssh key")
parser.add_argument('--remote-user-name', default='ubuntu', help="the remote machine user name")
parser.add_argument('--inventory-script', default=inventory_script, help="path to EC2 inventory script")

args = parser.parse_args()

command = [args.inventory_script, '--tag-name', args.tag]
run_inventory = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
string_inventory, error = run_inventory.communicate('S\nL\n')

if error:
    raise Exception(error)
    exit(1)

inventory = json.loads(string_inventory.decode('utf-8'))

tags = list(filter(lambda tag: args.search_tag in tag, inventory.keys()))

print_with_indexes(tags)

if len(tags) > 1:
    print('enter number of %s (defualt 0):' % args.tag)
    index = input()
    index = int(index) if index else 0
elif len(tags) == 1:
    index = 0
else:
    raise Exception("no such role")

tag = tags[index]

hosts = inventory[tag].get('hosts')
host = hosts[0]

if not args.no_ssh:
    os.system('ssh -i %s %s@%s' % (args.ssh_key, args.remote_user_name, host))
else:
    print(host)
