### prerequisites
- your EC2 instances most have a `role` tag, by which you can ask for them.
- you should have the instances `.pem` key at `~/.ssh/keypair.pem`.
- you should have a `~/.aws/keys` with the following content: ```
  {  
      "AWSAccessKeyId": "<access-key>",
      "AWSSecretKey": "<secret-key>",
      "region": "<regaion>"
  }
- your remote user-name is `ubuntu` (:)).

### install
- clone repository into ~/.scripts
- install python(3) requirments `sudo pip3 install ./requirments.txt`

### usage
assuming you have an EC2 instance with tag `role` with value `big-baa`, run `./ssh_by_role.py big`.

