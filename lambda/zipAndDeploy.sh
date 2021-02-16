. venv/bin/activate
rm -rf lambda-dev-*
export ZAPPA_LAMBDA_PACKAGE="$(cut -d' ' -f3 <<< `zappa package dev | tail -n 1`)"
deactivate
cd ..
. .venv/bin/activate
ZAPPA_LAMBDA_PACKAGE=$ZAPPA_LAMBDA_PACKAGE cdk deploy
deactivate
cd lambda
