ec2-dns-monitor
===============

Create a Python Lambda function to create DNS records in Route53 of your EC2 instances IP addresses. This is useful if you use a lot of short lived EC2 instances for which you would like to have an easy DNS name. The Lambda script gets triggered by an AWS Config rule which triggers whenever the tag of an EC2 instance is edited. It then checks all EC2 instances for the 'DNS' tag and uses these to create DNS records for all running EC2 instances.  


Contact
-------

For any questions or fixes, please reach out to @marekq! 
