from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda as lambdacons,
    aws_apigateway as apigwcons,
    aws_ec2 as ec2,
)
from constructs import Construct

class LambdavpcStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
         # The code that defines your stack goes here

        self.mylambda = lambdacons.Function(
            self,"HelloLambdafunc",
            runtime = lambdacons.Runtime.PYTHON_3_7,
            code = lambdacons.Code.from_asset('lambdacode'),
            handler = "hello.handler",
        )
        # apigwcons.LambdaRestApi(
        #     self, 'Endpoint',
        #     handler=self.mylambda,
        # )
        
