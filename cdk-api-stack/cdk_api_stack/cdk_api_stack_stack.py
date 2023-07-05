from constructs import Construct
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
)

# from cdk_dynamo_table_view import TableViewer
from .hitcounter import HitCounter

class CdkApiStackStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Defines an AWS Lambda resource
        my_lambda = _lambda.Function(
            self, 'LambdaHandler',
            runtime=_lambda.Runtime.PYTHON_3_10,
            code=_lambda.Code.from_asset('lambda'),
            handler='my-lambda.handler',
        )

        hello_with_counter = HitCounter(
            self, 'HitCounter',
            downstream=my_lambda,
        )

        apigw.LambdaRestApi(
            self, 'Endpoint',
            handler=hello_with_counter._handler,
        )