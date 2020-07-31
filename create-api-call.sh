#!/bin/bash
## Create bucket 
echo "Create bucket..."
aws s3api create-bucket \
--bucket jaf-deploy \
--region sa-east-1 \
--create-bucket-configuration LocationConstraint=sa-east-1

echo "Create bucket..."
aws s3api create-bucket \
--bucket jaf-artifactory \
--region sa-east-1 \
--create-bucket-configuration LocationConstraint=sa-east-1

## Send app to s3
echo "Upload..."
aws s3 cp bulk-scheduler-1.1.zip s3://jaf-deploy/lambdas/

## Create Stack
aws cloudformation create-stack \
--region sa-east-1 \
--stack-name hlg-bulk-api \
--template-body file://cf-codebuild-slack-notification.yml \
--parameters file://parameters.json \
--capabilities CAPABILITY_NAMED_IAM 

## Requirements
pip install -r requirements.txt -t .