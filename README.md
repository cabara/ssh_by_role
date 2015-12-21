### Prerequisites
- Your EC2 instances must have a `role` tag, by which you can ask for them.
- You should have the instances `.pem` key at `~/.ssh/keypair.pem`.
- You should have a `~/.aws/keys` with the following content: `
    {  
        "AWSAccessKeyId": "<access-key>",
        "AWSSecretKey": "<secret-key>",
        "region": "<regaion>"
    }
`
- Your remote user-name is `ubuntu` (:)).

### Install
- Clone repository into ~/.scripts
- Install python(3) requirments `sudo pip3 install ./requirments.txt`

### Usage
Assuming you have an EC2 instance with tag `role` and value `big-baa`, run `./ssh_by_role.py big`.

