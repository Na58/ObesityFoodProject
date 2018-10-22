'''depend: Python
	sudo apt-get update
	sodu apt-get install python-boto\
	pip install boto'''

import boto 


avail_zone = 'us-east-2'


#my cloud
access_key = 'access_key'
secret_key = 'secret_key'


conn = boto.ec2.connect_to_region(avail_zone, aws_access_key_id=access_key, aws_secret_access_key=secret_key)

def get_conn():
	return conn































