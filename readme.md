ec2-dns-monitor
===============

Create a Python Lambda function to create DNS records in Route53 of your EC2 instances IP addresses. This is useful if you use a lot of short lived EC2 instances for which you would like to have an easy DNS name. The Lambda script gets triggered by an AWS Config rule which triggers whenever the tag of an EC2 instance is edited. It then checks all  instances for the 'DNS' tag and uses these to create DNS records for all running EC2 instances through Route53.  

Below a simple schematic overview of the architecture;


![alt tag](https://raw.githubusercontent.com/marekq/ec2-dns-monitor/master/docs/1.jpg)


Installation
------------

First off, make sure you have a valid and working Route53 zone deployed in the account where you will use the Lambda function. You will need to configure the name of the zone within the environment variable of the Lambda function, it is used to ensure we are writing DNS record to the correct DNS zone (in my case, I simply enter 'marek.rocks' as the FQDN). If you make a typo or the zone doesn't exist, the Lambda function will stop itself. 

I recommmend to use the  Serverless framework to push the function, a serverless.yml file is available which can push the code to S3, configure the environment variables and properties of the Lambda function for you. To install the function using Serverless, simply type "serverless deploy" within the root directory of the tool. Please remember to change the default zone name in "serverless.yml" to match yours. 

You can also install the code manually by uploading the content of "getdns.py" and setting the environment variable "zone" manually in the Lambda console. You will need to configure the Lambda function to use Python and have 128MB memory available. 

In addition, ensure the Lambda execution role can describe EC2 instances and that it has write access to the Route53 zone. You could use a custom IAM policy such as the one below to achieve this.

Once your Lambda script is set up, create an instance tag in the EC2 console and call it DNS - we will set the hostname we want the instance to have here;


![alt tag](https://raw.githubusercontent.com/marekq/ec2-dns-monitor/master/docs/2.jpg)


Now you should be able to run the Lambda code and see if it succesfully created the records in Route53. The CloudWatch events should provide you with an overview of created records;

```bash
found hosted zone 		marek.rocks.
route53 dns zones 		marek.rocks.

created DNS A record 	test.marek.rocks 				-> 52.18.x.x
created DNS A record 	anewdnsrecord.marek.rocks 		-> 34.252.x.x
```

Backlog
-------

- Check whether new DNS records need to be added instead of always overwriting them. This is not a huge performance impact if you use just a handfull of EC2 instances, but it would be good practice to either cache or lookup the DNS zone before making writes to it.  
- Deploy and trigger automatically whenever an AWS Config rule triggers a tag change on EC2. This would indicate the script needs to rerun again and check if there are new/changed DNS tags set on one of the instances, meaning the DNS record the user sets becomes available in a few seconds after the instance launches. 
- Automatically deploy the correct IAM roles for the Lambda function so that the user doesn't have to do so. 
- Automatically deploy the AWS Config rule and the SNS topic for the user using CloudFormation. 
- Write the full "FQDN" tag to the EC2 instance once a DNS record was created, so the user knows what the public DNS name is. 


Contact
-------

For any questions or fixes, please reach out to @marekq! 
