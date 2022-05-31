# Project: sign-aws-lambda-packages-as-upload-to-aws-s3
AWS Lambda project which an AWS S3 Event Notification triggers, that allows you to sign Lambda packages when they're uploaded to AWS S3.

# Setup (AWS):
https://medium.com/@jean.velez2/automatically-sign-your-aws-lambda-packages-9c4599aea844

# Steps:
1. Grabs the S3 bucket and object name the S3 event notification provides.
2. Signs the S3 object with AWS Signer and stores it in the same bucket for different folder.
3. Creates a copy of the Signed S3 object with its original name in the destination path.
4. Delete original signed package name.

## Reference
 https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html
 https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html