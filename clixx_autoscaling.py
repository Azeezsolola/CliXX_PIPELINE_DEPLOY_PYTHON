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
response=subnet.subnet.create_subnet(
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
response=subnet.subnet.create_subnet(
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
response=subnet.subnet.create_subnet(
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
response=subnet.subnet.create_subnet(
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
response=subnet.subnet.create_subnet(
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
response=subnet.subnet.create_subnet(
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
response=subnet.subnet.create_subnet(
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
response=subnet.subnet.create_subnet(
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
response=subnet.subnet.create_subnet(
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
response=subnet.subnet.create_subnet(
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
response=subnet.subnet.create_subnet(
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
response=subnet.subnet.create_subnet(
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



