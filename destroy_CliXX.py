#!/usr/bin/python

import boto3,botocore,time

AWS_REGION='us-east-1'

sts_client=boto3.client('sts')

#Calling the assume_role function
assumed_role_object=sts_client.assume_role(RoleArn='arn:aws:iam::495599767034:role/Engineer', RoleSessionName='mysession')

credentials=assumed_role_object['Credentials']

print(credentials)





#--------------------Calling ssm to get value of RDS id -------------------------------------------

ssm=boto3.client('ssm',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = ssm.get_parameter(Name='/myapp/rdsidentifier', WithDecryption=True)
rdsvalue=response['Parameter']['Value']
print(rdsvalue)

#Deleting RDS
rds_client=boto3.client('rds',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = rds_client.delete_db_instance(
    DBInstanceIdentifier=rdsvalue,
    SkipFinalSnapshot=True
    )

time.sleep(400)



#---------------Caling ssm to get load balacer arn -------------------------------------------

ssm=boto3.client('ssm',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = ssm.get_parameter(Name='/myapp/loadbalancer', WithDecryption=True)
loadbalancerarn=response['Parameter']['Value']
print(loadbalancerarn)

#Deleting Load Balancer
elb=boto3.client('elbv2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = elb.delete_load_balancer(
    LoadBalancerArn=loadbalancerarn
)

time.sleep(60)


#-----------------Calling ssm to get target group info----------------------------------------------------

ssm=boto3.client('ssm',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = ssm.get_parameter(Name='/myapp/targetgroup', WithDecryption=True)
targetgroup=response['Parameter']['Value']
print(targetgroup)

#Deleting target group
elb2=boto3.client('elbv2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = elb2.delete_target_group(
    TargetGroupArn=targetgroup
)

time.sleep(60)




#-----------calling ssm to get autos caling group info ------------------------------------------

ssm=boto3.client('ssm',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = ssm.get_parameter(Name='/myapp/austoscaling', WithDecryption=True)
autoscaling_groupname=response['Parameter']['Value']
print(autoscaling_groupname)


#Deleting Autoscaling group
autoscaling = boto3.client('autoscaling', aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response =autoscaling.delete_auto_scaling_group(
    AutoScalingGroupName=autoscaling_groupname,
    ForceDelete=True
)



#-------------------Deleting mount targets -----------------------------------------------------------------

ssm=boto3.client('ssm',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = ssm.get_parameter(Name='/myapp/mounttarget', WithDecryption=True)
mounttarget=response['Parameter']['Value']
print(mounttarget)



mount_target_ids = mounttarget.split(',')

for mount_target_id in mount_target_ids:
    mount_target_id = mount_target_id.strip() 
    efs=boto3.client('efs',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
    response = efs.delete_mount_target(
            MountTargetId=mount_target_id
        )


time.sleep(120)


#---------------------calling ssm to get file syatem info -------------------------------------------------------


ssm=boto3.client('ssm',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = ssm.get_parameter(Name='/myapp/filesystem', WithDecryption=True)
filesystem=response['Parameter']['Value']
print(filesystem)

#Deleting File system
efs=boto3.client('efs',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = efs.delete_file_system(
    FileSystemId=filesystem
)




#---------calling ssm to get nat gateway info ------------------------------------------------

ssm=boto3.client('ssm',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = ssm.get_parameter(Name='/myapp/natgateway', WithDecryption=True)
nat=response['Parameter']['Value']
print(nat)


#Delete NAT 
natgate=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = natgate.delete_nat_gateway(
    DryRun=False,
    NatGatewayId=nat
)

time.sleep(60)


#---------Deleting ptivate sub1--------------------------------------------------
ssm=boto3.client('ssm',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = ssm.get_parameter(Name='/myapp/privsubid1', WithDecryption=True)
priv1=response['Parameter']['Value']
print(priv1)

sub=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = sub.delete_subnet(
    SubnetId=priv1,
    DryRun=False
)


time.sleep(60)


#-----------Deleting pub subnet 1-----------------------------------------
ssm=boto3.client('ssm',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = ssm.get_parameter(Name='/myapp/pubsubid1', WithDecryption=True)
pub1=response['Parameter']['Value']
print(pub1)

sub=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = sub.delete_subnet(
    SubnetId=pub1,
    DryRun=False
)

time.sleep(60)

#---------------------------Deleting private subnet 2 -------------------------------------------
ssm=boto3.client('ssm',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = ssm.get_parameter(Name='/myapp/privsubnet2', WithDecryption=True)
priv2=response['Parameter']['Value']
print(priv2)

sub=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = sub.delete_subnet(
    SubnetId=priv2,
    DryRun=False
)

time.sleep(60)


#------------------------Deleting pub subnet 2----------------------------------------------------

ssm=boto3.client('ssm',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = ssm.get_parameter(Name='/myapp/pubsub2', WithDecryption=True)
pub2=response['Parameter']['Value']
print(pub2)

sub=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = sub.delete_subnet(
    SubnetId=pub2,
    DryRun=False
)

time.sleep(60)

#-------------------------Deleting route table 1 --------------------------------

ssm=boto3.client('ssm',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = ssm.get_parameter(Name='/myapp/routetable1', WithDecryption=True)
rt1=response['Parameter']['Value']
print(rt1)

routetab=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = routetab.delete_route_table(
        DryRun=False,
        RouteTableId=rt1
    )


time.sleep(60)

#------------------------Deleting route table 2 -----------------------------------------

ssm=boto3.client('ssm',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = ssm.get_parameter(Name='/myapp/routetable2', WithDecryption=True)
rt2=response['Parameter']['Value']
print(rt2)

routetab2=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = routetab2.delete_route_table(
        DryRun=False,
        RouteTableId=rt2
    )


time.sleep(60)
#------------------Deleting rds subnet group name---------------------------------------------------------------
ssm=boto3.client('ssm',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = ssm.get_parameter(Name='/myapp/subgroupname', WithDecryption=True)
subgn=response['Parameter']['Value']
print(subgn)

rds_client=boto3.client('rds',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = rds_client.delete_db_subnet_group(
    DBSubnetGroupName=subgn
)


time.sleep(60)
#-------------------------------Delete SG--------------------------------------------------------------------------
ssm=boto3.client('ssm',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = ssm.get_parameter(Name='/myapp/securitygroupid1', WithDecryption=True)
sg1=response['Parameter']['Value']
print(sg1)

SG=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = SG.delete_security_group(
    GroupId=sg1,
    GroupName='pubsubnetSG',
    DryRun=False
)

#----------------------------------------Delecting SG--------------------------------------------------------------------------
ssm=boto3.client('ssm',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = ssm.get_parameter(Name='/myapp/securitygroupid2', WithDecryption=True)
sg2=response['Parameter']['Value']
print(sg2)

SG2=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = SG2.delete_security_group(
    GroupId=sg2,
    GroupName='privatesubnetSG',
    DryRun=False
)



#------calling to get template info --------------------------------------------------------

ssm=boto3.client('ssm',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = ssm.get_parameter(Name='/myapp/launchtemp', WithDecryption=True)
template=response['Parameter']['Value']
print(template)

#Delete TEmplatae 
LT=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = LT.delete_launch_template(
    DryRun=False,
    LaunchTemplateId=template
    
)

time.sleep(180)
#---------------------------Detaching internet gateway from vpc -------------------------------------
ssm=boto3.client('ssm',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = ssm.get_parameter(Name='/myapp/internet', WithDecryption=True)
internet=response['Parameter']['Value']
print(internet)

ssm=boto3.client('ssm',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = ssm.get_parameter(Name='/myapp/vpcid', WithDecryption=True)
vpc=response['Parameter']['Value']
print(vpc)

igw=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response=igw.detach_internet_gateway(
        InternetGatewayId=internet,
        VpcId=vpc
)


#-----------------------------Deleting Internet Gateway-----------------------------------------------
ssm=boto3.client('ssm',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = ssm.get_parameter(Name='/myapp/internet', WithDecryption=True)
internet=response['Parameter']['Value']
print(internet)



igw=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = igw.delete_internet_gateway(
    DryRun=False,
    InternetGatewayId=internet
)

time.sleep(300)

#-----------------calling ssm to vpc info ----------------------------------

ssm=boto3.client('ssm',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = ssm.get_parameter(Name='/myapp/vpcid', WithDecryption=True)
vpc=response['Parameter']['Value']
print(vpc)

#Delete VPC
vpc1=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = vpc1.delete_vpc(
    VpcId=vpc,
    DryRun=False
)






