# ssh_ec2.py

let's you easily ssh login to your EC2 machines.

---
#### options
to see all options run `./ssh_ec2.py --help`.
#### Prerequisites
- Your EC2 instances must have a `role` tag, by which you can ask for them. this option is the default you can choose your own tag with the `--tag` option.
- You should have the instances `.pem` key at `~/.ssh/keypair.pem`. this option is the default you can specify your own ssh key with the `--ssh-key` option.
- You should have a `~/.aws/keys` with the following content:
  `{  
        "AWSAccessKeyId": "<access-key>",
        "AWSSecretKey": "<secret-key>",
        "region": "<regaion>"
  }`.
  this is only for the shipped with, EC2 inventory script, you can supply your own script with the `--inventory` option.

#### Install
- Clone repository into ~/.scripts
- Install python(3) requirments `sudo pip3 install ./requirments.txt`

#### Usage
Assuming you have an EC2 instance with tag `role` and value `big-baa`, run `./ssh_by_role.py big`.
