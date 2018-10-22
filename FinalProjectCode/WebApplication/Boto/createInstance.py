import boto 
import time

import connector

#live Security Group
#['ssh','https','couchdb','erlang','icpm']


def create_instance():
	ec2_conn = connector.get_conn()
	avail_zone = 'us-east-2'
	
	print "creating instance"
	instance_pool = ec2_conn.run_instances('ami-0782e9ee97725263d', #imageID
							key_name = 'A1',
							instance_type = 't2.micro') 
	
	instance = instance_pool.instances[0]
	
	print "end of execution"

create_instance()