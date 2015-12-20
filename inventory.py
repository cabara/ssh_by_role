#!/usr/bin/python
"""
script excpects to have the following json format files:
    - ~/.aws/keys:
        {  
          "AWSAccessKeyId": "fjasdfjdkslfjaldslkfa",
          "AWSSecretKey": "jfdajlfdksjaljfajklfdjklfdas"
        }
    - .slack:
        {
            "token": "sdfjkkldjsafjklfdsjkladfsjklfd"
        }
    - .bitbucket/credentials:
        {
            "user": "baaaaaaa",
            "password": "badfjsdkljkfl"
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
    slack_token_path = os.path.join(home, '.slack')
    bitbucket_keys_path = os.path.join(home, '.bitbucket/credentials')


    aws_keys = open_config_file(aws_keys_path)
    slack_token = open_config_file(slack_token_path)
    bitbucket_credentials = open_config_file(bitbucket_keys_path)

    cabara_keys_path = os.path.join(home, '.aws/cabara_production')
    cabara_keys = json.load(open(cabara_keys_path))

    global_vars = {
        "aws": cabara_keys,
        "slack": slack_token,
        "statsd_host": "statsd.cabaraproduction.com",
        "bitbucket_user": bitbucket_credentials.get('user')
    }

    conn = boto.ec2.connect_to_region(
        "us-west-2",
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
                if tag == "monitor":
                    global_vars["graphite_host"] = instance.dns_name
                if tag == 'domains-mongo-data':
                    global_vars["data_mongo"] = instance.dns_name
                inventory[tag]["hosts"].append(instance.dns_name)

    for role in inventory.keys():
        inventory[role]['vars'] = dict(global_vars) # make a copy
        inventory[role]['vars']['role'] = role
    return json.dumps(inventory, indent=4)


cache = get_cache()
if cache:
    inventory = cache
else:
    inventory = get_inventory()
    write_cache(inventory)
print(inventory)
