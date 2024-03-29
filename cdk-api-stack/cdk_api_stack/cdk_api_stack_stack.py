# this file defines the cdk stack
# a layer, a lambda function, an api gateway and an api gateway handler

from constructs import Construct
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
)
import os
from dotenv import load_dotenv

load_dotenv()

# from cdk_dynamo_table_view import TableViewer
from .hitcounter import HitCounter

class CdkApiStackStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        #  defining a Lambda Layer that includes your custom module
        co2_layer = _lambda.LayerVersion(
            self, "MyCustomLayer",
            code=_lambda.Code.from_asset(path="lambda/co2"),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_10]  # Adjust the runtime as needed
        )

        # defining an AWS Lambda resource
        my_lambda = _lambda.Function(
            self, 'LambdaHandler',
            runtime=_lambda.Runtime.PYTHON_3_10,
            code=_lambda.Code.from_asset('lambda'),
            handler='my-lambda.handler',
            environment={
                'FRONTEND_URL': os.getenv('FRONTEND_URL'),
                'CO2_ST_URL': os.getenv('CO2_ST_URL'),
                'CO2_ST_API_KEY': os.getenv('CO2_ST_API_KEY'),
                'CO2_T_URL': os.getenv('CO2_T_URL')
            },
            layers=[co2_layer]  # Add the custom layer to the Lambda function
        )

        # defining a handler for the api gateway, which uses the lambda as a downstream
        hello_with_counter = HitCounter(
            self, 'HitCounter',
            downstream=my_lambda,
        )

        # defining an api gateway to be hit
        api = apigw.LambdaRestApi(
            self, 'Endpoint',
            handler=hello_with_counter._handler,
        )