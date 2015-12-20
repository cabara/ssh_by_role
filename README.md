### prerequisites
- your EC2 instances most have a `role` tag, by which you can ask for them.
- you should have the instances `.pem` key at `~/.ssh/keypair.pem`.
- your remove user-name is `ubuntu` (:)).

### install
- clone repository into ~/.scripts
- install python(3) requirments `sudo pip3 install ./requirments.txt`

### usage
assuming you have an EC2 instance with tag `role` with value `big-baa`, run `./ssh_by_role.py big`.

