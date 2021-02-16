#!/usr/bin/env python3

from aws_cdk import core

from cdk_flask.cdk_flask_stack import CdkFlaskStack


app = core.App()
CdkFlaskStack(app, "cdk-flask")

app.synth()
