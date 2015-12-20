#!/usr/bin/python
"""
scripts expects json file at: `~/.aws/keys`
with content:
    {  
          "AWSAccessKeyId": "fjasdfjdkslfjaldslkfa",
          "AWSSecretKey": "jfdajlfdksjaljfajklfdjklfdas",
          "region": "us-west-2"
    }
"""

import os
import json
import time
import boto.ec2


def write_cache(inventory):
    cache_file = open('./.inventory.cache', 'w')
    cache_file.write(inventory)
    cache_file.close()

def get_cache():
    try:
        cache_file_stats = os.stat('./.inventory.cache')
        if time.time() - cache_file_stats.st_mtime > 3 * 60:
            return None
        cache_file = open('./.inventory.cache', 'r')
        return cache_file.read()
    except:
        return None


def open_config_file(path):
    try:
        return json.load(open(path))
    except IOError:
        print('you are missing a config file at: %s' % path)
    except ValueError:
        print('your json is not well formatted:\n"""\n%s\n"""' % open(path).read())

def get_inventory():
    home = os.environ['HOME']

    aws_keys_path = os.path.join(home, '.aws/keys')
    aws_keys = open_config_file(aws_keys_path)

    conn = boto.ec2.connect_to_region(
        aws_keys['region'],
        aws_access_key_id=aws_keys['AWSAccessKeyId'],
        aws_secret_access_key=aws_keys['AWSSecretKey']
    )

    instances = filter(
        lambda instance: instance.dns_name,
        reduce(
            lambda instcs1, instcs2: instcs1 + instcs2,
            map(
                lambda reservation: reservation.instances,
                conn.get_all_instances()
            ),
            []
        )
    )

    inventory = {}

    for instance in instances:
        if instance.tags.get('role'):
            for tag in instance.tags.get('role', '').split(','):
                if not inventory.get(tag):
                    inventory[tag] = {
                        "hosts": []
                    }
                inventory[tag]["hosts"].append(instance.dns_name)

    return json.dumps(inventory, indent=4)


cache = get_cache()
if cache:
    inventory = cache
else:
    inventory = get_inventory()
    write_cache(inventory)

print(inventory)
