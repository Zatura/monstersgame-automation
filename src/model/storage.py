import logging
import boto3
from botocore.exceptions import ClientError
from auth.s3 import region_name, aws_access_key_id, aws_access_key_secret


class Storage:
    def __init__(self):
        self.s3_client = boto3.client('s3',
                                      region_name=region_name,
                                      aws_access_key_id=aws_access_key_id,
                                      aws_secret_access_key=aws_access_key_secret)

    def create_bucket(self, bucket_name, region=None):
        try:
            if region is None:
                self.s3_client.create_bucket(Bucket=bucket_name)
            else:
                self.s3_client = boto3.client('s3', region_name=region)
                location = {'LocationConstraint': region}
                self.s3_client.create_bucket(Bucket=bucket_name,
                                             CreateBucketConfiguration=location)
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def upload_file(self, file_name, bucket='monstersgame', object_name=None):
        if object_name is None:
            object_name = file_name

        try:
            response = self.s3_client.upload_file(file_name, bucket, object_name)
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def download_file(self, filename, key, bucket='monstersgame'):
        try:
            response = self.s3_client.download_file(Filename=filename,
                                                    Key=key,
                                                    Bucket=bucket)
        except ClientError as e:
            logging.error(e)
            return False
        return True
