import boto3
import os

# AWS Clients & Resource
signer_client = boto3.client('signer')
s3_resource = boto3.resource('s3')
s3_client = boto3.client('s3')

# Variables
signer_profile = os.environ['SIGNER_PROFILE_NAME']
signed_path = 'signed/' # S3 path where signed packages are going to be stored

def lambda_handler(event, context):
    for records in event['Records']:
        s3_record = records['s3']
        bucket_name = s3_record['bucket']['name']
        bucket_object = s3_record['object']
        
        # Only zip files  and versioned objects in S3 are to be signed.
        if bucket_object['key'].endswith('.zip') and 'versionId' in bucket_object:
            signed_object = sign_lambda_package(bucket_name, bucket_object)
            rename_signed_lambda_package(bucket_name, bucket_object, signed_object)
          
# Sign the S3 object with AWS Signer profile.            
def sign_lambda_package(bucket_name, bucket_object):
    # Sign S3 Object and place it in the Same bucket but in a different path
    signing_job = signer_client.start_signing_job(
        source={
            's3': {
                'bucketName': bucket_name,
                'key': bucket_object['key'],
                'version': bucket_object['versionId']
            }
        },
        destination={
            's3': {
                'bucketName': bucket_name,
                'prefix': signed_path
            }
        },
        profileName='Signer_Test'
    )
    
    # Signed S3 object
    signed_object = signed_path + signing_job['jobId'] + '.zip'
    return signed_object

def rename_signed_lambda_package(bucket_name, bucket_object, signed_object):
    copy_source = {
        'Bucket': bucket_name,
        'Key': signed_object
    }
    
    # Retrieves S3 object name from Event data and creates another signed object with the retrieved S3 object name.
    s3_destination_object = bucket_object['key'].split('/')[-1]
    s3_resource.meta.client.copy(copy_source, bucket_name, signed_path + s3_destination_object)
    
    # Remove the original signed object
    response = s3_client.delete_object(
        Bucket=bucket_name,
        Key=signed_object,
    )