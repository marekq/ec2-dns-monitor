#!/usr/bin/python
# marek kuczynski
# @marekq
# www.marek.rocks

import boto3, os

# get the zone id of the DNS zone defined in Lambda environment
def get_r53_zid(c, zone):
	global zonid
	r 	= c.list_hosted_zones()
	l 	= []

	for y in range(len(r['HostedZones'])):
		zname 	= r['HostedZones'][y]['Name']
		zid 	= r['HostedZones'][y]['Id']
		l.append(zname)

		if zone == zname or zone+'.' == zname:
			zonid 	= zid

	# check if the zone name the user specifies exists
	if zonid != '':
		print 'found hosted zone \t'+zone+'\nroute53 dns zones \t'+', '.join(l)+'\n'
		get_ec2(c, zone)
	else:
		print 'no valid hosted zone found in route 53, fix this in your lambda environment variables!\n\nyou entered zone name as variable \t'+zone+'.\nzone names available in route53 \t'+', '.join(l)+'\n\nquitting...'


# retrieve the hosted zone of the Route53 account and return the Route53 session
def get_r53_sess():
	c   	= boto3.client('route53')
	return c


# add a DNS record to Route 53 based
def add_dns_rec(c, rname, ip, zone):
	d  		= c.change_resource_record_sets(HostedZoneId = zonid, 
		ChangeBatch 	= {
	        'Changes': [
	            {
	                'Action': 'UPSERT',
	                'ResourceRecordSet': {
	                    'Name': rname+'.'+zone+'.',
	                    'Type': 'A',
	                    'TTL': 60,
	                    'ResourceRecords': [
	                        {
	                            'Value': ip
	                        },
	                    ],
	                }
	            },
	        ]
	    }
	)
	print 'created DNS A record \t '+rname+'.'+zone+' \t -> '+ip


# get all running ec2 instances
def get_ec2(d, zone):
	c 	= boto3.client('ec2')
	r 	= c.describe_instances(Filters = [{'Name':'instance-state-name','Values':['running']}])
	x 	= r['Reservations']

	# create DNS records by reading the 'DNS' tag of every EC2 instance and adding the public IP to Route 53
	for y in x:
		for z in y['Instances'][0]['Tags']:
			if z['Key'] == 'DNS':
				iip 		= y['Instances'][0]['PublicIpAddress']
				iid 		= y['Instances'][0]['InstanceId']
				add_dns_rec(d, z['Value'], iip, zone)


# the lambda handler that kicks off the script
def lambda_handler(event, context):
	zone 	= os.environ['zone']
	d 		= get_r53_sess()
	get_r53_zid(d, zone)
