#!/usr/bin/python

import boto3,botocore,base64,time

AWS_REGION='us-east-1'


sts_client=boto3.client('sts')

#Calling the assume_role function
assumed_role_object=sts_client.assume_role(RoleArn='arn:aws:iam::495599767034:role/Engineer', RoleSessionName='mysession')

credentials=assumed_role_object['Credentials']

print(credentials)


#--------------------------------------------------------Creating VPC-------------------------------------------------------------------------------------------------------------
VPC=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = VPC.create_vpc(
    CidrBlock='10.0.0.0/16',
    TagSpecifications=[
        {
            'ResourceType': 'vpc',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'STACKVPC'
                }
            ]
        }
    ],
    DryRun=False,
    InstanceTenancy='default',
    AmazonProvidedIpv6CidrBlock=False
)

print(response)
vpcid=response['Vpc']['VpcId']
print(vpcid)


#------------------------------Storing VPCID in SSM PARAMETER-----------------------------------------------------------------
ssm = boto3.client('ssm',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)

response = ssm.put_parameter(
    Name='/myapp/vpcid',
    Value=vpcid,
    Type='String',
    Overwrite=True
)

print(response)

#--------------Enabling VPC DNS Resolution-------------------------
vpcresolution=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = vpcresolution.modify_vpc_attribute(
    EnableDnsHostnames={
        'Value': True
    },
    VpcId=vpcid,
    
)
print(vpcresolution)

#---------------Enabling DNS support in the VPC----------------------------
vpcresolution2=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = vpcresolution2.modify_vpc_attribute(
    EnableDnsSupport={
        'Value': True
     },
    VpcId=vpcid
)
    
print(vpcresolution2)

#---------------------------Creating private subnet 1 for clixx instacne-------------------------------------------
subnet=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response=subnet.create_subnet(
    TagSpecifications=[
        {
            'ResourceType': 'subnet',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'privatesubnet1-clixx'
                }
            ]
        }
    ],
    AvailabilityZone='us-east-1a',
    CidrBlock='10.0.1.0/24',
    VpcId=vpcid,
    DryRun=False
)
print(response)
privatesubnet1clixxid=response['Subnet']['SubnetId']
print(privatesubnet1clixxid)

#-----------------------------------------------Calling ssm to store private subnet id -------------------------------------
ssm = boto3.client('ssm',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = ssm.put_parameter(
    Name='/myapp/privatesubnetclixx-1',
    Value=privatesubnet1clixxid,
    Type='String',
    Overwrite=True
)

print(response)

#-----------------------------Creating private subnet 2 for Clixx instances ---------------------------------------------
subnet=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response=subnet.create_subnet(
    TagSpecifications=[
        {
            'ResourceType': 'subnet',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'privatesubnet2-clixx'
                }
            ]
        }
    ],
    AvailabilityZone='us-east-1b',
    CidrBlock='10.0.12.0/24',
    VpcId=vpcid,
    DryRun=False
)
print(response)
privatesubnet2clixxid=response['Subnet']['SubnetId']
print(privatesubnet2clixxid)

#-----------------------------Calling ssm parameter to store the clixx private subnet id ---------------------------------------
ssm = boto3.client('ssm',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = ssm.put_parameter(
    Name='/myapp/privatesubnetclixx-2',
    Value=privatesubnet2clixxid,
    Type='String',
    Overwrite=True
)

print(response)


#------------------------Creating public subnet 1 for load Balancer --------------------------------------------------------------
subnet=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response=subnet.create_subnet(
    TagSpecifications=[
        {
            'ResourceType': 'subnet',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'publicsubnet1-loadbalancer'
                }
            ]
        }
    ],
    AvailabilityZone='us-east-1a',
    CidrBlock='10.0.2.0/23',
    VpcId=vpcid,
    DryRun=False
)
print(response)
publicsubnet1loadbalancerid=response['Subnet']['SubnetId']
print(publicsubnet1loadbalancerid)

#-------------------------Calling ssm parameter to store the value for public subnet 1 -------------------------------------------
ssm = boto3.client('ssm',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = ssm.put_parameter(
    Name='/myapp/publicsubnetloadbalancer-1',
    Value=publicsubnet1loadbalancerid,
    Type='String',
    Overwrite=True
)

print(response)


#------------------------Creating public subnet 2 for load balancer ---------------------------------------------------------------
subnet=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response=subnet.create_subnet(
    TagSpecifications=[
        {
            'ResourceType': 'subnet',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'publicsubnet2-loadbalancer'
                }
            ]
        }
    ],
    AvailabilityZone='us-east-1b',
    CidrBlock='10.0.4.0/23',
    VpcId=vpcid,
    DryRun=False
)
print(response)
publicsubnet2loadbalancerid=response['Subnet']['SubnetId']
print(publicsubnet2loadbalancerid)

#----------------------Calling ssm to store the value for public subnet 2 -------------------------------------------------------
ssm = boto3.client('ssm',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = ssm.put_parameter(
    Name='/myapp/publicsubnetloadbalancer-2',
    Value=publicsubnet2loadbalancerid,
    Type='String',
    Overwrite=True
)

print(response)


#--------------------------Creating private subnet for RDS DataBase ---------------------------------------------------------------
subnet=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response=subnet.create_subnet(
    TagSpecifications=[
        {
            'ResourceType': 'subnet',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'privatesubnetRDSEFS1'
                }
            ]
        }
    ],
    AvailabilityZone='us-east-1a',
    CidrBlock='10.0.8.0/22',
    VpcId=vpcid,
    DryRun=False
)
print(response)
privatesubnetRDSEFS1=response['Subnet']['SubnetId']
print(privatesubnetRDSEFS1)


#-----------------------Calling ssm to store the rds databse subnet id -------------------------------------------------------------
ssm = boto3.client('ssm',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = ssm.put_parameter(
    Name='/myapp/privatesubnetRDSEFS-1',
    Value=privatesubnetRDSEFS1,
    Type='String',
    Overwrite=True
)

print(response)


#----------------------Creating orivates subnet for RDS and EFS 2 ------------------------------------------------------------------
subnet=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response=subnet.create_subnet(
    TagSpecifications=[
        {
            'ResourceType': 'subnet',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'privatesubnetRDSEFS2'
                }
            ]
        }
    ],
    AvailabilityZone='us-east-1b',
    CidrBlock='10.0.16.0/22',
    VpcId=vpcid,
    DryRun=False
)
print(response)
privatesubnetRDSEFS2=response['Subnet']['SubnetId']
print(privatesubnetRDSEFS2)

#-----------------Calling ssm to store the rds subnet id ------------------------------------------------------------------------------
ssm = boto3.client('ssm',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = ssm.put_parameter(
    Name='/myapp/privatesubnetRDSEFS-2',
    Value=privatesubnetRDSEFS2,
    Type='String',
    Overwrite=True
)

print(response)

#----------------------Creatign private subnet to host oraclel DB---------------------------------------------------------------------
subnet=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response=subnet.create_subnet(
    TagSpecifications=[
        {
            'ResourceType': 'subnet',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'privatesubnetOracleDB1'
                }
            ]
        }
    ],
    AvailabilityZone='us-east-1a',
    CidrBlock='10.0.20.0/24',
    VpcId=vpcid,
    DryRun=False
)
print(response)
privatesubnetoracleDB1=response['Subnet']['SubnetId']
print(privatesubnetoracleDB1)

#-------------------Calling ssm to store the subnet id fir oracle Db subneet -------------------------------------------------------
ssm = boto3.client('ssm',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = ssm.put_parameter(
    Name='/myapp/privatesubnetoracleDB1',
    Value=privatesubnetoracleDB1,
    Type='String',
    Overwrite=True
)

print(response)

#-------------------------Creating private subnet 2 to host oracle DB---------------------------------------------------------------
subnet=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response=subnet.create_subnet(
    TagSpecifications=[
        {
            'ResourceType': 'subnet',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'privatesubnetOracleDB2'
                }
            ]
        }
    ],
    AvailabilityZone='us-east-1b',
    CidrBlock='10.0.21.0/24',
    VpcId=vpcid,
    DryRun=False
)
print(response)
privatesubnetoracleDB2=response['Subnet']['SubnetId']
print(privatesubnetoracleDB2)

#-----------------------Calling ssm to store the value of the subnet id for oracle DB 2--------------------------------------------
ssm = boto3.client('ssm',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = ssm.put_parameter(
    Name='/myapp/privatesubnetoracleDB2',
    Value=privatesubnetoracleDB2,
    Type='String',
    Overwrite=True
)

print(response)

#----------------------Creating Private subnet for to host Java App Database--------------------------------------------------------
subnet=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response=subnet.create_subnet(
    TagSpecifications=[
        {
            'ResourceType': 'subnet',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'privatesubnetjavaDB1'
                }
            ]
        }
    ],
    AvailabilityZone='us-east-1a',
    CidrBlock='10.0.22.0/26',
    VpcId=vpcid,
    DryRun=False
)
print(response)
privatesubnetjavadb1id=response['Subnet']['SubnetId']
print(privatesubnetjavadb1id)

#---------------------------------Calling ssm to store private subnet id for Java app Db--------------------------------------------
ssm = boto3.client('ssm',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = ssm.put_parameter(
    Name='/myapp/privatesubnetjavadb1',
    Value=privatesubnetjavadb1id,
    Type='String',
    Overwrite=True
)

print(response)

#--------------------Creating private subnet 2 for java app DB--------------------------------------------------------------------
subnet=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response=subnet.create_subnet(
    TagSpecifications=[
        {
            'ResourceType': 'subnet',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'privatesubnetjavaDB2'
                }
            ]
        }
    ],
    AvailabilityZone='us-east-1b',
    CidrBlock='10.0.23.0/26',
    VpcId=vpcid,
    DryRun=False
)
print(response)
privatesubnetjavadb2id=response['Subnet']['SubnetId']
print(privatesubnetjavadb2id)

#------------------------Ssm to store the sbove subnet id----------------------------------------------------------------------------
ssm = boto3.client('ssm',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = ssm.put_parameter(
    Name='/myapp/privatesubnetjavadb2',
    Value=privatesubnetjavadb2id,
    Type='String',
    Overwrite=True
)

print(response)

#----------------------Creating Private subnet to host Java app instances-------------------------------------------------
subnet=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response=subnet.create_subnet(
    TagSpecifications=[
        {
            'ResourceType': 'subnet',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'privatesubnetjavaapp1'
                }
            ]
        }
    ],
    AvailabilityZone='us-east-1a',
    CidrBlock='10.0.24.0/26',
    VpcId=vpcid,
    DryRun=False
)
print(response)
privatesubnetjavaapp1id=response['Subnet']['SubnetId']
print(privatesubnetjavaapp1id)

#----------------------Calling ssm to store the above subnet id ------------------------------------------------------------
ssm = boto3.client('ssm',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = ssm.put_parameter(
    Name='/myapp/privatesubnetjava1',
    Value=privatesubnetjavaapp1id,
    Type='String',
    Overwrite=True
)

print(response)

#-----------------------creating private subnet 2 for java instances ------------------------------------------------------
subnet=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response=subnet.create_subnet(
    TagSpecifications=[
        {
            'ResourceType': 'subnet',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'privatesubnetjavaapp2'
                }
            ]
        }
    ],
    AvailabilityZone='us-east-1b',
    CidrBlock='10.0.25.0/26',
    VpcId=vpcid,
    DryRun=False
)
print(response)
privatesubnetjavaapp2id=response['Subnet']['SubnetId']
print(privatesubnetjavaapp2id)

#-----------------Calling smm to store the above subnet id -----------------------------------------------------------------
ssm = boto3.client('ssm',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = ssm.put_parameter(
    Name='/myapp/privatesubnetjava2',
    Value=privatesubnetjavaapp2id,
    Type='String',
    Overwrite=True
)

print(response)


#----------------------Creating Internet Gateway ------------------------------------------------------------------------
internetgateway=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response =internetgateway.create_internet_gateway(
    TagSpecifications=[
        {
            'ResourceType': 'internet-gateway',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'publicinternetgateway'
                }
            ]
        }
    ],
    DryRun=False
)

print(response)
intgwid=response['InternetGateway']['InternetGatewayId']
print(intgwid)


#------------------Calling ssm to store internet gateway id -------------------------------------------------------------
ssm = boto3.client('ssm',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = ssm.put_parameter(
    Name='/myapp/internetgateway',
    Value=intgwid,
    Type='String',
    Overwrite=True
)

print(response)

#----------------Attaching Inetrnet Gateway to VPC---------------------------------------------------------------------
internetattach=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = internetattach.attach_internet_gateway(
    DryRun=False,
    InternetGatewayId=intgwid,
    VpcId=vpcid
)
print(response)


#----------------------Creating NAT Gateway----------------------------------------------------------------------------------
NAT=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = NAT.create_nat_gateway(
    AllocationId='eipalloc-0fdf690c8a3ba0e89',
    DryRun=False,
    SubnetId=publicsubnet1loadbalancerid,
    TagSpecifications=[
        {
            'ResourceType': 'natgateway',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'NATGW'
                }
            ]
        }
    ]
    
)
print(response)
natid=response['NatGateway']['NatGatewayId']
print(natid)
time.sleep(120)

#--------------------Storing NAT Gaetway Id in ssm 0-----------------------------------------------------------------
ssm = boto3.client('ssm',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = ssm.put_parameter(
    Name='/myapp/natgateway',
    Value=natid,
    Type='String',
    Overwrite=True
)

print(response)

#-------------------------Creating public subnet route table---------------------------------------------------------------
RT=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = RT.create_route_table(
    TagSpecifications=[
        {
            'ResourceType': 'route-table',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'publicroutetable'
                }
            ]
        }
    ],
    DryRun=False,
    VpcId=vpcid
)

print(response)
routetableid=response['RouteTable']['RouteTableId']
print(routetableid)

time.sleep(120)

#----------Calling ssm to store public route table id --------------------------------------------------------------------
ssm = boto3.client('ssm',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = ssm.put_parameter(
    Name='/myapp/routetable1',
    Value=routetableid,
    Type='String',
    Overwrite=True
)

print(response)

#----------------------Creating entry in the route table ------------------------------------------------------------------
publicRTENTRY=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = publicRTENTRY.create_route(
    RouteTableId=routetableid,       
    DestinationCidrBlock='0.0.0.0/0',  
    GatewayId=intgwid                   
)
print(response)


#-------------------Creating Private Route table -------------------------------------------------------------------------
RT2=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = RT2.create_route_table(
    TagSpecifications=[
        {
            'ResourceType': 'route-table',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'privateroutetable'
                }
            ]
        }
    ],
    DryRun=False,
    VpcId=vpcid
)
print(response)
privateroutetableid=response['RouteTable']['RouteTableId']
print(privateroutetableid)

time.sleep(120)

#------------------------Calling ssm to store route table id ----------------------------------------------------------------
ssm = boto3.client('ssm',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = ssm.put_parameter(
    Name='/myapp/routetable2',
    Value=privateroutetableid,
    Type='String',
    Overwrite=True
)

print(response)

#---------------------Creating entry in the private route table ---------------------------------------------------------------------
privateRTENTRY=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = privateRTENTRY.create_route(
    RouteTableId=privateroutetableid,       
    DestinationCidrBlock='0.0.0.0/0',  
    NatGatewayId=natid                  
)
print(response)

#----------------------Associating public route table with public subnet 1 -----------------------------------------------------------
igwass=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = igwass.associate_route_table(
    #GatewayId=intgwid,
    DryRun=False,
    SubnetId=publicsubnet1loadbalancerid,
    RouteTableId=routetableid
)

print(response)

#----------------------Associating public route table with public subnet 2 -----------------------------------------------------------
Asspub2=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response =Asspub2.associate_route_table(
    #GatewayId=intgwid,
    DryRun=False,
    SubnetId=publicsubnet2loadbalancerid,
    RouteTableId=routetableid
)

print(response)


#--------------------Associating Private route table with all private subnets ----------------------------------------------------------
Assprivate1=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response =Assprivate1.associate_route_table(
    #GatewayId=intgwid,
    DryRun=False,
    SubnetId=privatesubnet1clixxid,
    RouteTableId=privateroutetableid
)

print(response)

Assprivate2=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response =Assprivate2.associate_route_table(
    #GatewayId=intgwid,
    DryRun=False,
    SubnetId=privatesubnet2clixxid,
    RouteTableId=privateroutetableid
)

print(response)

Assprivate3=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response =Assprivate3.associate_route_table(
    #GatewayId=intgwid,
    DryRun=False,
    SubnetId=privatesubnetRDSEFS1,
    RouteTableId=privateroutetableid
)

print(response)

Assprivate4=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response =Assprivate3.associate_route_table(
    #GatewayId=intgwid,
    DryRun=False,
    SubnetId=privatesubnetRDSEFS2,
    RouteTableId=privateroutetableid
)

print(response)

Assprivate5=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response =Assprivate5.associate_route_table(
    #GatewayId=intgwid,
    DryRun=False,
    SubnetId=privatesubnetoracleDB1,
    RouteTableId=privateroutetableid
)

print(response)

Assprivate6=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response =Assprivate6.associate_route_table(
    #GatewayId=intgwid,
    DryRun=False,
    SubnetId=privatesubnetoracleDB2,
    RouteTableId=privateroutetableid
)

print(response)

Assprivate7=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response =Assprivate7.associate_route_table(
    #GatewayId=intgwid,
    DryRun=False,
    SubnetId=privatesubnetjavadb1id,
    RouteTableId=privateroutetableid
)

print(response)

Assprivate8=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response =Assprivate8.associate_route_table(
    #GatewayId=intgwid,
    DryRun=False,
    SubnetId=privatesubnetjavadb2id,
    RouteTableId=privateroutetableid
)

print(response)

Assprivate9=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response =Assprivate9.associate_route_table(
    #GatewayId=intgwid,
    DryRun=False,
    SubnetId=privatesubnetjavaapp1id,
    RouteTableId=privateroutetableid
)

print(response)

Assprivate10=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response =Assprivate10.associate_route_table(
    #GatewayId=intgwid,
    DryRun=False,
    SubnetId=privatesubnetjavaapp2id,
    RouteTableId=privateroutetableid
)

print(response)



#-------------------------Creating Security Group For lOad Balancer ----------------------------------------------------
pubsg=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = pubsg.create_security_group(
    Description='public_subnet_SG',
    GroupName='publicsubnetSG1',
    VpcId=vpcid,
    TagSpecifications=[
        {
            'ResourceType': 'security-group',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'loadbalancersecuritygroup'
                }
            ]
        }
    ],
    DryRun=False
)
print(response)
pubsgid=response['GroupId']
print(pubsgid)

#---------------------Calling ssm to store security group id -------------------------------------------------------
ssm = boto3.client('ssm',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = ssm.put_parameter(
    Name='/myapp/securitygroupid1',
    Value=pubsgid,
    Type='String',
    Overwrite=True
)

print(response)

#--------------------Adding rules to load Balancer security group-------------------------------------------------------
pubrule1=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response=pubrule1.authorize_security_group_ingress(
    GroupId=pubsgid,
    IpPermissions=[
        {
            'IpProtocol': 'tcp',
            'FromPort': 443,
            'ToPort': 443,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]  
        }
    ]
)



pubrule2=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response=pubrule2.authorize_security_group_ingress(
    GroupId=pubsgid,
    IpPermissions=[
        {
            'IpProtocol': 'tcp',
            'FromPort': 22,
            'ToPort': 22,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]  
        }
    ]
)


#------------Creating security group for EC2 instances -------------------------------------------------------------
clixxprivsq1=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = clixxprivsq1.create_security_group(
    Description='private_subnet_SG',
    GroupName='privatesubnetSG1',
    VpcId=vpcid,
    TagSpecifications=[
        {
            'ResourceType': 'security-group',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'clixxapplication_SG'
                }
            ]
        }
    ],
    DryRun=False
)
print(response)
clixxappsqid=response['GroupId']
print(clixxappsqid)


#---------------------Calling ssm to store ec2 instances security group id -------------------------------------------------------
ssm = boto3.client('ssm',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = ssm.put_parameter(
    Name='/myapp/clixxapplicationsg1',
    Value=clixxappsqid,
    Type='String',
    Overwrite=True
)

print(response)


#----------------Creating security group for RDS and EFS --------------------------------------------------------------------
rdsefsprivsq1=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = rdsefsprivsq1.create_security_group(
    Description='private_subnet_SG',
    GroupName='privatesubnetSG2',
    VpcId=vpcid,
    TagSpecifications=[
        {
            'ResourceType': 'security-group',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'rdsefs_SG'
                }
            ]
        }
    ],
    DryRun=False
)
print(response)
rdsefsid=response['GroupId']
print(rdsefsid)

#-------------------Calling ssm to store rds and efs security group id --------------------------------------------------------------------
ssm = boto3.client('ssm',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = ssm.put_parameter(
    Name='/myapp/rdsefssg',
    Value=rdsefsid,
    Type='String',
    Overwrite=True
)

print(response)


#----------------Adding Rules to ec2 instance security group---------------------------------------------------------------
addrules1=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response=addrules1.authorize_security_group_ingress(
    GroupId=clixxappsqid,
    IpPermissions=[
        {
            'IpProtocol': 'tcp',
            'FromPort': 22,
            'ToPort': 22,
            'IpRanges': [{'CidrIp': '10.0.2.0/23'}]  
        }
    ]
)

addrules2=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response=addrules2.authorize_security_group_ingress(
    GroupId=clixxappsqid,
    IpPermissions=[
        {
            'IpProtocol': 'tcp',
            'FromPort': 3306,
            'ToPort': 3306,
            'UserIdGroupPairs': [{'GroupId': pubsgid}]  
        }
    ]
)

addrules3=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response=addrules3.authorize_security_group_ingress(
    GroupId=clixxappsqid,
    IpPermissions=[
        {
            'IpProtocol': 'tcp',
            'FromPort': 2049,
            'ToPort': 2049,
            'UserIdGroupPairs': [{'GroupId': pubsgid}]  
        }
    ]
)

addrules4=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response=addrules4.authorize_security_group_ingress(
    GroupId=clixxappsqid,
    IpPermissions=[
        {
            'IpProtocol': 'tcp',
            'FromPort': 2049,
            'ToPort': 2049,
            'UserIdGroupPairs': [{'GroupId': rdsefsid}]  
        }
    ]
)

addrules5=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response=addrules5.authorize_security_group_ingress(
    GroupId=clixxappsqid,
    IpPermissions=[
        {
            'IpProtocol': 'tcp',
            'FromPort': 80,
            'ToPort': 80,
            'UserIdGroupPairs': [{'GroupId': pubsgid}]  
        }
    ]
)



#------------------Adding Rules to RDS and EFS security group ------------------------------------------------------------------------
addrules6=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response=addrules6.authorize_security_group_ingress(
    GroupId=rdsefsid,
    IpPermissions=[
        {
            'IpProtocol': 'tcp',
            'FromPort': 3306,
            'ToPort': 3306,
            'UserIdGroupPairs': [{'GroupId': clixxappsqid}]  
        }
    ]
)

addrules7=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response=addrules7.authorize_security_group_ingress(
    GroupId=rdsefsid,
    IpPermissions=[
        {
            'IpProtocol': 'tcp',
            'FromPort': 2049,
            'ToPort': 2049,
            'UserIdGroupPairs': [{'GroupId': clixxappsqid}]  
        }
    ]
)

addrules8=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response=addrules8.authorize_security_group_ingress(
    GroupId=rdsefsid,
    IpPermissions=[
        {
            'IpProtocol': 'tcp',
            'FromPort': 2049,
            'ToPort': 2049,
            'UserIdGroupPairs': [{'GroupId': pubsgid}]  
        }
    ]
)

addrules9=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response=addrules9.authorize_security_group_ingress(
    GroupId=rdsefsid,
    IpPermissions=[
        {
            'IpProtocol': 'tcp',
            'FromPort': 3306,
            'ToPort': 3306,
            'UserIdGroupPairs': [{'GroupId': pubsgid}]  
        }
    ]
)


#----------------------Creating load Balancer in public subnet------------------------------------------------------------------------
elb=boto3.client('elbv2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = elb.create_load_balancer(
    Name='autoscalinglb2-azeez',
    Subnets=[publicsubnet1loadbalancerid,publicsubnet2loadbalancerid],
    SecurityGroups=[pubsgid],
    Scheme='internet-facing',
    
    Tags=[
        {
            'Key': 'OwnerEmail',
            'Value': 'azeezsolola14+development@outlook.com'
        },
    ],
    Type='application',
    IpAddressType='ipv4'
    )

print(response)
loadbalancerarn=response["LoadBalancers"][0]["LoadBalancerArn"]
print(loadbalancerarn)
LBDNS=response["LoadBalancers"][0]["DNSName"]
print(LBDNS)

ELBZONEID=response["LoadBalancers"][0]["CanonicalHostedZoneId"]
print(ELBZONEID)

time.sleep(300)

#------------------------Calling ssm parameter to store Load balancer arn--------------------------------------------------------
ssm = boto3.client('ssm',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = ssm.put_parameter(
    Name='/myapp/loadbalancer',
    Value=loadbalancerarn,
    Type='String',
    Overwrite=True
)

print(response)


#-----------------------------Creating Target Group------------------------------------

response = elb.create_target_group(
    Name='clixxautoscalingtg2',
    Protocol='HTTP',
    ProtocolVersion='HTTP1',
    Port=80,
    VpcId=vpcid,
    HealthCheckProtocol='HTTP',
    HealthCheckEnabled=True,
    HealthCheckIntervalSeconds=300,
    HealthCheckTimeoutSeconds=120,
    HealthCheckPort='80',
    HealthCheckPath='/',
    HealthyThresholdCount=2,
    UnhealthyThresholdCount=5,
    TargetType='instance',
    Matcher={
        'HttpCode': "200,301"
        
    },
    
    IpAddressType='ipv4'
)

targetgrouparn=response['TargetGroups'][0]['TargetGroupArn']
print(targetgrouparn)


#----------------------Calling ssm parameter to store target group id -------------------------------

ssm = boto3.client('ssm',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = ssm.put_parameter(
    Name='/myapp/targetgroup',
    Value=targetgrouparn,
    Type='String',
    Overwrite=True
)

print(response)

#------------------------Creating listner on load balancer and attaching taregt group-------------------------

elb1 = boto3.client('elbv2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = elb1.create_listener(
    LoadBalancerArn=loadbalancerarn, 
    Port=443,
    Protocol='HTTPS',
    Certificates=[  
        {
            'CertificateArn': 'arn:aws:acm:us-east-1:495599767034:certificate/c4b0e3bc-b06f-42f5-b26b-e631e9720f8a'  
        }
    ],
    DefaultActions=[
        {
            'Type': 'forward',
            'TargetGroupArn': targetgrouparn  
        }
    ]
)
listener_arn = response['Listeners'][0]['ListenerArn']
print(listener_arn)


#------------------------------tie domain name with lb DNS--------------------------------------

route53=boto3.client('route53',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = route53.change_resource_record_sets(
    HostedZoneId='Z0099082ZFVZUBLTJX9D',
    ChangeBatch={
        'Comment': 'update_DNS',
        'Changes': [
            {
                'Action': 'UPSERT',
                'ResourceRecordSet': {
                    'Name': 'dev.clixx-azeez.com',
                    'Type': 'A',
                    'AliasTarget': {
                            'HostedZoneId': ELBZONEID,  
                            'DNSName': LBDNS,
                            'EvaluateTargetHealth': False
                        }
 
                }
            }
        ]
    }
)

print(response)


#----------------------creating efs --------------------------------------

efs=boto3.client('efs',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
# Create a file system
response = efs.create_file_system(
    CreationToken='devfs', 
    PerformanceMode='generalPurpose',  
    Encrypted=True,  
    ThroughputMode='elastic',  
    Backup=False,  
    Tags=[
        {
            'Key': 'Name',  
            'Value': 'azeezefs'
        },
    ]
)

print(response)
filesystemid=response["FileSystemId"]
print(filesystemid)

time.sleep(300)



#---------------------------------Creating Target mounts and Attaching Security group to efs --------------------------------------
filesystemid=response["FileSystemId"]
security_group_id=rdsefsid
mount_target_ids = []
subnet_ids = [privatesubnetRDSEFS1,privatesubnetRDSEFS2]
mounttarget=boto3.client('efs',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
for subnet_id in subnet_ids:
  response=mounttarget.create_mount_target(
        FileSystemId=filesystemid,
        SubnetId=subnet_id,
        SecurityGroups=[rdsefsid]
    )
  mount_target_id = response['MountTargetId']
  mount_target_ids.append(mount_target_id)
print(mount_target_ids)



#----------------------CAlling ssm to store filesystem id ---------------------------------------------

ssm = boto3.client('ssm',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = ssm.put_parameter(
    Name='/myapp/filesystem',
    Value=filesystemid,
    Type='String',
    Overwrite=True
)

print(response)

mount_target_ids_str = ",".join(mount_target_ids)
ssm = boto3.client('ssm',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = ssm.put_parameter(
    Name='/myapp/mounttarget',
    Value=mount_target_ids_str,
    Type='StringList',
    Overwrite=True
)

print(response)


#---------------------------------Creating RDS group for RDS DB----------------------------------

rdsdbsub = boto3.client('rds',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = rdsdbsub.create_db_subnet_group(
    DBSubnetGroupName='rdsdbsubgroup',
    DBSubnetGroupDescription='Two private subnets',
    SubnetIds=[privatesubnetRDSEFS1,privatesubnetRDSEFS2],
    Tags=[
            {
                'Key': 'Name',
                'Value': 'rdsdbsubnetgroup'
            }
            
        ]
)
print(response)

#---------------------------------calling ssm to store rds groupname ----------------------------

ssm = boto3.client('ssm',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = ssm.put_parameter(
    Name='/myapp/subgroupname',
    Value='rdsdbsubgroup',
    Type='String',
    Overwrite=True
)

print(response)

#------------------------------Create RDS DB-----------------------------------------

rds_client = boto3.client('rds',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
# Restore DB instance from snapshot
response = rds_client.restore_db_instance_from_db_snapshot(
    DBInstanceIdentifier='wordpressdbclixx-ecs2',
    DBSnapshotIdentifier='arn:aws:rds:us-east-1:577701061234:snapshot:wordpressdbclixx-ecs-snapshot',
    DBInstanceClass='db.m6gd.large',
    DBSubnetGroupName='rdsdbsubgroup',
    MultiAZ=True,
    PubliclyAccessible=True,
    VpcSecurityGroupIds=[rdsefsid]
    )
print(response)

time.sleep(600)

#--------------------Calling ssm to store rds id ----------------------------------------
ssm = boto3.client('ssm',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = ssm.put_parameter(
    Name='/myapp/rdsidentifier',
    Value='wordpressdbclixx-ecs2',
    Type='String',
    Overwrite=True
)

print(response)


FILE=filesystemid
MOUNT_POINT="/var/www/html"
REGION='us-east-1'
LB_NS='https://dev.clixx-azeez.com'
WP_CONFIG_PATH="/var/www/html/wp-config.php"
CONDITIONAL_STATEMENT="if (isset(\$_SERVER['HTTP_X_FORWARDED_PROTO']) && \$_SERVER['HTTP_X_FORWARDED_PROTO'] === 'https') {\\n \$_SERVER['HTTPS'] = 'on';\\n}"




#Creating Launch Template 

AWS_REGION='us-east-1'
USER_DATA = """#!/bin/bash

##Install the needed packages and enable the services(MariaDb, Apache)
sudo yum update -y

sudo mkdir -p {mount_point}
sudo chown ec2-user:ec2-user {mount_point}
echo "{file}.efs.{region}.amazonaws.com:/ {mount_point} nfs4 nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,_netdev 0 0" | sudo tee -a /etc/fstab
sleep 300
sudo mount -a 


sudo systemctl start httpd
sudo systemctl enable httpd
sudo systemctl is-enabled httpd
 
##Add ec2-user to Apache group and grant permissions to /var/www
sudo usermod -a -G apache ec2-user
sudo chown -R ec2-user:apache /var/www
sudo chmod 2775 /var/www && find /var/www -type d -exec sudo chmod 2775 {{}} \;
find /var/www -type f -exec sudo chmod 0664 {{}} \;
cd /var/www/html

if [ -f /var/www/html/wp-config.php ]
then
    echo "wp-config.php already exists"
    
else
    echo "wp-config.php does not exist"
    git clone https://github.com/stackitgit/CliXX_Retail_Repository.git
fi
        


#git clone https://github.com/stackitgit/CliXX_Retail_Repository.git
cp -r CliXX_Retail_Repository/* /var/www/html
## Allow wordpress to use Permalinks
sudo sed -i '151s/None/All/' /etc/httpd/conf/httpd.conf
sudo sed -i 's/wordpress-db.cc5iigzknvxd.us-east-1.rds.amazonaws.com/wordpressdbclixx-ecs2.cn2yqqwoac4e.us-east-1.rds.amazonaws.com/' /var/www/html/wp-config.php

if [ $? == 0 ]
then
    echo "sed was done"
else
    echo "sed was not done"
fi

sudo sed -i.bak "/That's all, stop editing!/i {condition}" {wp}
if [ $? == 0 ]
then
    echo "sed for condtional statement was done"
else
    echo "sed for condtional statement was not done"
fi

#DNS=$(curl http://169.254.169.254/latest/meta-data/public-hostname)
#echo $DNS
#DNS=${lb_dns}
sleep 600
output_variable=$(mysql -u wordpressuser -p -h wordpressdbclixx-ecs2.cn2yqqwoac4e.us-east-1.rds.amazonaws.com -D wordpressdb -pW3lcome123 -sse "select option_value from wp_options where option_value like 'CliXX-APP-%';")
echo $output_variable

if [ output_variable == {lb_dns} ]
then
    echo "DNS Address in the the table"
else
    echo "DNS Address is not in the table"
    #Logging DB
    mysql -u wordpressuser -p -h wordpressdbclixx-ecs2.cn2yqqwoac4e.us-east-1.rds.amazonaws.com -D wordpressdb -pW3lcome123<<EOF
    UPDATE wp_options SET option_value ="{lb_dns}" WHERE option_value LIKE "CliXX-APP-%";
EOF
fi


##Grant file ownership of /var/www & its contents to apache user
sudo chown -R apache /var/www

##Grant group ownership of /var/www & contents to apache group
sudo chgrp -R apache /var/www

##Change directory permissions of /var/www & its subdir to add group write 
sudo chmod 2775 /var/www
find /var/www -type d -exec sudo chmod 2775 {{}} \;

##Recursively change file permission of /var/www & subdir to add group write perm
sudo find /var/www -type f -exec sudo chmod 0664 {{}} \;

##Restart Apache
sudo systemctl restart httpd
sudo service httpd restart

##Enable httpd 
sudo systemctl enable httpd 
sudo /sbin/sysctl -w net.ipv4.tcp_keepalive_time=200 net.ipv4.tcp_keepalive_intvl=200 net.ipv4.tcp_keepalive_probes=5

""".format(file=FILE, region=REGION, mount_point=MOUNT_POINT, lb_dns=LB_NS, condition=CONDITIONAL_STATEMENT, wp=WP_CONFIG_PATH)


encoded_user_data = base64.b64encode(USER_DATA.encode('utf-8')).decode('utf-8')

ec2=boto3.client('ec2',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response=ec2.create_launch_template(
    DryRun=False,
    LaunchTemplateName='oloyede',
    VersionDescription='webserver1',
    LaunchTemplateData={
        'EbsOptimized': True,     
        'ImageId': 'ami-056d6c51d3b7d21af',
        'InstanceType': 't2.micro',  
        'KeyName': 'Azeez10',     
        'UserData': encoded_user_data,
        #'SecurityGroupIds': [pubsgid],
        'NetworkInterfaces': [{
            'AssociatePublicIpAddress': False,  
            'DeviceIndex': 0,
            'SubnetId': privatesubnet1clixxid,
            'Groups': [clixxappsqid] 
        }]
    }
    )

    
print(response)
launchtempid=response["LaunchTemplate"]["LaunchTemplateId"]
print(launchtempid)

launchtempname=response["LaunchTemplate"]["LaunchTemplateName"]
print(launchtempname)


#-------------------------------Calling ssm to store template id -------------------------

ssm = boto3.client('ssm',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = ssm.put_parameter(
    Name='/myapp/launchtemp',
    Value=launchtempid,
    Type='String',
    Overwrite=True
)

print(response)


#------------------------------tie domain name with lb DNS--------------------------------------

route53=boto3.client('route53',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = route53.change_resource_record_sets(
    HostedZoneId='Z0099082ZFVZUBLTJX9D',
    ChangeBatch={
        'Comment': 'update_DNS',
        'Changes': [
            {
                'Action': 'UPSERT',
                'ResourceRecordSet': {
                    'Name': 'dev.clixx-azeez.com',
                    'Type': 'A',
                    'AliasTarget': {
                            'HostedZoneId': ELBZONEID,  
                            'DNSName': LBDNS,
                            'EvaluateTargetHealth': False
                        }
 
                }
            }
        ]
    }
)

print(response)




#-----------------------------Creating autoscaling---------------------------------

autoscaling = boto3.client('autoscaling', aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = autoscaling.create_auto_scaling_group(
    AutoScalingGroupName='my-auto-scaling-group',
    
    LaunchTemplate={
        'LaunchTemplateId': launchtempid
        
       
    },
    
    
    MinSize=1,
    MaxSize=3,
    DesiredCapacity=1,
    DefaultCooldown=300,
 

    TargetGroupARNs=[targetgrouparn],
  
    HealthCheckGracePeriod=300,
   
   
    Tags=[
        {
           
            'Key': 'Name',
            'Value': 'newinstance',
            'PropagateAtLaunch': True
        }
    ],
   
    
   
    DefaultInstanceWarmup=300,
    VPCZoneIdentifier = f"{privatesubnet1clixxid},{privatesubnet2clixxid}"

     #VPCZoneIdentifier=[publicsubnetid,publicsubnetid2]

 
)

print(response)


#--------------------------Calling ssm to store auto scalingroup id  -----------------------------

ssm = boto3.client('ssm',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = ssm.put_parameter(
    Name='/myapp/austoscaling',
    Value='my-auto-scaling-group',
    Type='String',
    Overwrite=True
)

print(response)

#-------------------------------------creating Scale out policy-------------------------------------

autoscaling = boto3.client('autoscaling', aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
scale_up_policy = autoscaling.put_scaling_policy(
    AutoScalingGroupName='my-auto-scaling-group',
    PolicyName='ScaleUpPolicy',
    AdjustmentType='ChangeInCapacity',
    ScalingAdjustment=1,  
    Cooldown=30  
)
print(scale_up_policy)



#---------------------------------------Creating SCale Down Policy-------------------------------------

autoscaling = boto3.client('autoscaling', aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
scale_down_policy = autoscaling.put_scaling_policy(
    AutoScalingGroupName='my-auto-scaling-group',
    PolicyName='ScaleDownPolicy',
    AdjustmentType='ChangeInCapacity',
    ScalingAdjustment=-1,  
    Cooldown=30
)
print(scale_down_policy)





#-------------------------------------Scale up alarm----------------------------------------

cloudwatch = boto3.client('cloudwatch',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response=cloudwatch.put_metric_alarm(
    AlarmName='CPUUtilizationHigh',
    MetricName='CPUUtilization',
    Namespace='AWS/EC2',
    Statistic='Average',
    Period=300,
    EvaluationPeriods=1,
    Threshold=50.0,  
    ComparisonOperator='GreaterThanThreshold',
    Dimensions=[
        {
            'Name': 'AutoScalingGroupName',
            'Value': 'my-auto-scaling-group'
        },
    ],
    ActionsEnabled=True,
    AlarmActions=[
        scale_up_policy['PolicyARN']  
    ]
)
print(response)



#-------------------------------------Scale down alarm--------------------------------------

autoscaling = boto3.client('autoscaling', aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response=cloudwatch.put_metric_alarm(
    AlarmName='CPUUtilizationLow',
    MetricName='CPUUtilization',
    Namespace='AWS/EC2',
    Statistic='Average',
    Period=300,
    EvaluationPeriods=1,
    Threshold=25.0,  
    ComparisonOperator='LessThanThreshold',
    Dimensions=[
        {
            'Name': 'AutoScalingGroupName',
            'Value': 'my-auto-scaling-group'
        },
    ],
    ActionsEnabled=True,
    AlarmActions=[
        scale_down_policy['PolicyARN']  
    ]
)
print(response)



#----------------------Creating SNS TOPIC for RDS HIGH CPU USAGE-----------------------------------------
sns = boto3.client('sns',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = sns.create_topic(
    Name='High_RDS_CPU_USAGE'
   
)
print(response)
topic_arn = response['TopicArn']
print(topic_arn)

#----------------Creating subscription for sns topic above-----------------------------------------------
sns2 = boto3.client('sns',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = sns2.subscribe(
    TopicArn=topic_arn,
    Protocol='email',
    Endpoint='azeezsolola14@outlook.com',
    ReturnSubscriptionArn=True
)

#-------Calling ssm paramater to store sns arn-----------------------------------------------------------------
ssm10 = boto3.client('ssm',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = ssm10.put_parameter(
    Name='/myapp/snstopicforRDS',
    Value= topic_arn,
    Type='String',
    Overwrite=True
)

print(response)

#------------------Creatin alarm for high rds cpu usage-----------------------------------------------------
alarm1 = boto3.client('cloudwatch',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)

response = alarm1.put_metric_alarm(
        AlarmName="HighCPUutilization",
        ComparisonOperator="GreaterThanThreshold",
        EvaluationPeriods=300,
        MetricName='CPUUtilization',
        Namespace='AWS/RDS',
        Period=10,
        Statistic='Average',
        Threshold=50,
        ActionsEnabled=True,
        AlarmDescription="RDS CPU ABOVE 50%",
        Dimensions=[
            {
                'Name': 'DBInstanceIdentifier',
                'Value': "wordpressdbclixx-ecs2"
            },
        ],
        Unit='Percent',
        AlarmActions=[topic_arn]  # Specify the SNS topic ARN here
    )

alarm_name = 'HighCPUutilization'


#---------Calling ssm paramater to store alarm name----------------------------------------------------------------------
ssm13 = boto3.client('ssm',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = ssm13.put_parameter(
    Name='/myapp/snstopicforrdsalarm',
    Value= alarm_name ,
    Type='String',
    Overwrite=True
)

print(response)


#-------------------Creating sns topic for my instancing in autoscaling group--------------------------------------------------
sns3 = boto3.client('sns',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = sns3.create_topic(
    Name='High_INSTANCE_CPU_UTILIZATION_FOR_INSTANCES_IN_THE_AUTOSCALING_GROUP_BY_AZEEZ'
   
)
print(response)
topic_arn1 = response['TopicArn']
print(topic_arn1)

#-------Calling ssm paramater to store sns arn-----------------------------------------------------------------
ssm11 = boto3.client('ssm',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = ssm11.put_parameter(
    Name='/myapp/snstopicforautoscaling',
    Value= topic_arn1,
    Type='String',
    Overwrite=True
)

print(response)

#----------------Creating subscription for sns topic above-----------------------------------------------
sns22 = boto3.client('sns',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = sns22.subscribe(
    TopicArn=topic_arn1,
    Protocol='email',
    Endpoint='azeezsolola14@outlook.com',
    ReturnSubscriptionArn=True
)



#------------------Creating Alarm using CLoudwatch when instacne cpu utilization is greater than threshold---------------------------------------------------------------------------

cloudwatch = boto3.client('cloudwatch',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response=cloudwatch.put_metric_alarm(
    AlarmName='CPUUtilizationHigh',
    MetricName='CPUUtilization',
    Namespace='AWS/EC2',
    Statistic='Average',
    Period=300,
    EvaluationPeriods=1,
    Threshold=50.0,  
    ComparisonOperator='GreaterThanThreshold',
    Dimensions=[
        {
            'Name': 'AutoScalingGroupName',
            'Value': 'my-auto-scaling-group'
        },
    ],
    ActionsEnabled=True,
    AlarmActions=[ topic_arn1]
)
print(response)

alarm_name2 = 'CPUUtilizationHigh'

#--------Calling ssm to store alrm name for the above alarm------------------------------------------------------------------------
ssm14 = boto3.client('ssm',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = ssm14.put_parameter(
    Name='/myapp/snstopicforinstancealarm',
    Value= alarm_name2 ,
    Type='String',
    Overwrite=True
)


#------creating topic Load Balancer trackking------------------------------------------------------------------------------
sns76 = boto3.client('sns',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = sns76.create_topic(
    Name='Monitoring_Load_Balancer_BY_AZEEZ'
   
)
print(response)
topic_arn11 = response['TopicArn']
print(topic_arn11)


#-------Calling ssm paramater to store sns arn-----------------------------------------------------------------
ssm11 = boto3.client('ssm',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = ssm11.put_parameter(
    Name='/myapp/loadBalancaralarmtopicarn',
    Value= topic_arn11,
    Type='String',
    Overwrite=True
)

print(response)


#----------------Creating subscription for sns topic above-----------------------------------------------
sns22 = boto3.client('sns',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = sns22.subscribe(
    TopicArn=topic_arn11,
    Protocol='email',
    Endpoint='azeezsolola14@outlook.com',
    ReturnSubscriptionArn=True
)


cloud = boto3.client('cloudwatch',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response=cloud.put_metric_alarm(
        AlarmName='LoadBalancerAlarm',
        AlarmDescription='Tracking the number of Requests on load Balancer ',
        ActionsEnabled=True,
        MetricName='RequestCount',
        Namespace='AWS/ApplicationELB',
        Statistic='Sum',
        Period=60,
        EvaluationPeriods=1,
        Threshold=100,
        ComparisonOperator='GreaterThanThreshold',
        Dimensions=[
            {
                'Name': 'LoadBalancer',
                'Value': loadbalancerarn
            },
        ],
        AlarmActions=[topic_arn11],
       
        Unit='Count'
    )

print(response)

loadbalanceralarm='LoadBalancerAlarm'
#-------Calling ssm paramater to store the above alarm name -----------------------------------------------------------------
ssm11 = boto3.client('ssm',aws_access_key_id=credentials['AccessKeyId'],aws_secret_access_key=credentials['SecretAccessKey'],aws_session_token=credentials['SessionToken'],region_name=AWS_REGION)
response = ssm11.put_parameter(
    Name='/myapp/loadBalancaralarmname',
    Value= loadbalanceralarm,
    Type='String',
    Overwrite=True
)

print(response)

