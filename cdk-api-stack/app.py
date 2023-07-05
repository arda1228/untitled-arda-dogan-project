#!/usr/bin/env python3

import aws_cdk as cdk

from cdk_api_stack.cdk_api_stack_stack import CdkApiStackStack


app = cdk.App()
CdkApiStackStack(app, "cdk-api-stack")

app.synth()
