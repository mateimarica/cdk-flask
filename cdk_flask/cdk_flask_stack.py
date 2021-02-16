import os

from aws_cdk import (
	core,
	aws_lambda as _lambda,
	aws_apigateway as apigw,
	aws_apigateway as apigw,
	aws_dynamodb as dynamodb,
	aws_iam
)


class CdkFlaskStack(core.Stack):

	def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
		super().__init__(scope, construct_id, **kwargs)

        	# The code that defines your stack goes here

		dynamodb_table = self._create_ddb_table()

		flask_handler = _lambda.Function(
			self, 'FlaskHandler',
			description="Handles a Flask API for a sample CDK app",
			runtime=_lambda.Runtime.PYTHON_3_7,
			code=_lambda.Code.asset('lambda/' + os.environ["ZAPPA_LAMBDA_PACKAGE"]),
			function_name='ssm-cdk_flask_handler-dev-lf',
			handler='handler.lambda_handler',
			timeout=core.Duration.seconds(15),			
		)

		flask_handler.add_environment(
			'DYNAMODB_TABLE_NAME',
			dynamodb_table.table_name
		)

		lambda_policy_statement = aws_iam.PolicyStatement(
			resources=[dynamodb_table.table_arn],
			actions=[
				'dynamodb:GetItem',
				'dynamodb:PutItem',
				'dynamodb:UpdateItem',
				'dynamodb:DeleteItem',
				'dynamodb:Scan',
			],
		)

		flask_handler.add_to_role_policy(
			lambda_policy_statement
		)
	
		apigw.LambdaRestApi(
			self, 'Endpoint',
			description="A sample REST API for a Lambda function.",
			handler=flask_handler,
			rest_api_name='ssm-cdk_flask-dev-api'
		)
	
	
	def _create_ddb_table(self):
		dynamodb_table = dynamodb.Table(
			self, 'Users',
			partition_key=dynamodb.Attribute(
				name='username', type=dynamodb.AttributeType.STRING
			),
			removal_policy=core.RemovalPolicy.DESTROY,
			table_name='ssm-cdk_flask_users-dev'
		)

		core.CfnOutput(
			self,
			'AppTableName',
			value=dynamodb_table.table_name
		)

		return dynamodb_table
