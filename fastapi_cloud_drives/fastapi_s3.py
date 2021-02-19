from fastapi_cloud_drives.base_class import CloudStorageAbstractClass
import os
import sys
import threading

import logging
import boto3
from botocore.exceptions import ClientError


class S3:   
    def __init__(self, conf):
        self.session = boto3.session.Session()
        self.s3_client = boto3.resource("s3")

    async def upload_file(self, file_name: str, bucket: str, object_name=None, extra_args: dict=None):
        """Upload a file to an S3 bucket

        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :param extra_args: Metadata to attach to file. 
        :For information about Metadata: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html

        :return: True if file was uploaded, else False
        """
        s3_client = boto3.client('s3')

        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = file_name

        # Upload the file
        try:
            response = s3_client.upload_file(
                file_name,
                bucket,
                object_name,
                ExtraArgs = extra_args,
                Callback=ProgressPercentage(file_name)
                )
            print("response", response)
        except ClientError as e:
            logging.error(e)
            return False
        return True

    async def download_file(self, bucket_name: str, file_name: str, object_name: str=None, extra_args: dict=None):
        s3_client = self.session.resource("s3")

        s3_client.download_file(
            bucket_name,
            file_name,
            object_name,
            ExtraArgs = extra_args,
            Callback=ProgressPercentage(file_name)
            )

    async def list_buckets(self):
        """[List existing buckets]

        Returns:
            [dict]: [List of buckets]
        """
        s3_client = self.session.resource("s3")

        buckets = []
        for bucket in s3_client.buckets.all():
            buckets.append(bucket.name)
        return buckets

    async def create_bucket(self, bucket_name: str):
        """Create an S3 bucket in a specified region

        If a region is not specified, the bucket is created in the S3 default
        region (us-east-1).

        Args:
            bucket_name (str): [Bucket name to create bucket in s3]

        :param bucket_name: Bucket to create
        :param region: String region to create bucket in, e.g., 'us-west-2'
        :return: True if bucket created, else False
        """
        # Create bucket
        s3_client = self.session.resource("s3")
        try:
            if self.region is None:
                s3_client.create_bucket(Bucket=bucket_name)
            else:
                s3_client = boto3.client('s3', region_name=self.region)
                location = {'LocationConstraint': self.region}

                s3_client.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration=location
                    )

        except ClientError as e:
            logging.error(e)
            return False
        return True


class ProgressPercentage(object):

    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        # To simplify, assume this is hooked up to a single filename
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)" % (
                    self._filename, self._seen_so_far, self._size,
                    percentage))
            sys.stdout.flush()