host = "baaa.us-west-2.compute.amazonaws.com"
import os
os.system('ssh -i ~/.ssh/keypair.pem ubuntu@%s' % host)