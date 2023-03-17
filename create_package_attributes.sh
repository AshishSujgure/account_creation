#!/bin/bash

set -e
PACKAGE_NAME="lambda_get_dynamodb.zip"

if [ -f ${PACKAGE_NAME} ]; then
    rm -f ${PACKAGE_NAME}
fi

pip3.93.93.93.93.93.93.93.93.9 install -r requirements.txt --target ./package
cd package
zip -r ../${PACKAGE_NAME} .
cd ..
zip -g ${PACKAGE_NAME} lambda_function.py setData.py
