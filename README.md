### install

- clone repository into ~/.scripts
- you EC2 instances most have a `role` tag, by which you can ask for them.
- install python(3) requirments `sudo pip3 install ./requirments.txt`

### usage

assuming you have an EC2 instance with tag `role` with value `big-baa`, run `./ssh_by_role.py big`.

