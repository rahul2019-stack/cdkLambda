from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda as lambdacons,
    aws_apigateway as apigwcons,
    aws_ec2 as ec2,
)
from constructs import Construct

class NetworkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
         # The code that defines your stack goes here

        self.myvpc = ec2.Vpc(self, "rhyVpc" ,
                        max_azs = 2,
                        cidr = "10.0.0.0/16",
                        nat_gateways =1,
                        subnet_configuration=[
                            ec2.SubnetConfiguration(
                            subnet_type=ec2.SubnetType.PUBLIC,
                            name = "publicSubnetRhy",
                            cidr_mask = 24,
                        ),
                            ec2.SubnetConfiguration(
                            subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT,
                            name = "PrivateSubnetRhy",
                            cidr_mask = 24,
                        ),
                            ec2.SubnetConfiguration(
                            subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                            name = "IsolatedSubnetRhy",
                            cidr_mask = 24,   
                        )
                        ]
        )

        # add NACL rule to above VPC
        dbPort = 5432
        privateSubnet = self.myvpc.private_subnets
        publicSubnet = self.myvpc.public_subnets
        isolatedSubnet = self.myvpc.isolated_subnets

        isolatedNacl = ec2.NetworkAcl(self,"IsolatedDbNacl",
                        vpc = self.myvpc,
                        subnet_selection = ec2.SubnetSelection(subnets=isolatedSubnet)
                        )

        for id,subnet in enumerate(privateSubnet, start=1):
            isolatedNacl.add_entry("dbNaclIngress{0}".format(id*100),
                                    rule_number=id*100,
                                    cidr = ec2.AclCidr.ipv4(subnet.node.default_child.cidr_block),
                                    traffic = ec2.AclTraffic.tcp_port_range(dbPort ,dbPort),
                                    rule_action=ec2.Action.ALLOW,
                                    direction=ec2.TrafficDirection.INGRESS
                                    )

            isolatedNacl.add_entry("dbNaclEgress{0}".format(id*100),
                                    rule_number=id*100,
                                    cidr = ec2.AclCidr.ipv4(subnet.node.default_child.cidr_block),
                                    traffic = ec2.AclTraffic.tcp_port_range(1024, 65535),
                                    rule_action=ec2.Action.ALLOW,
                                    direction=ec2.TrafficDirection.EGRESS
                                    )