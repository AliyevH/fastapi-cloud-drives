import os
import sys
import threading

import logging
import boto3
from botocore.exceptions import ClientError
from oauth2client import file
from pathlib import Path


class S3:   
    def __init__(self, conf):
        self.region = conf.AWS_DEFAULT_REGION
        self.session = boto3.session.Session()
        self.s3_resource = self.session.resource("s3")
        self.s3_client = boto3.client("s3", self.region)


    async def upload_file(self, file_name: Path, bucket_name: str, object_name=None, extra_args: dict=None):
        """[summary]

        Args:
            file_name (Path): [Path to file]
            bucket_name (str): [Bucket to upload to]
            object_name ([type], optional): [S3 object name. If not specified then file_name is used]. Defaults to None.
            extra_args (dict, optional): [https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html]. Defaults to None.

        Returns:
            [type]: [description]
        """
       
        __s3_bucket = self.s3_resource.Bucket(bucket_name)

        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = file_name

        # Upload the file
        try:
            __s3_bucket.upload_file(
                file_name,
                object_name,
                ExtraArgs = extra_args,
                Callback=ProgressPercentage(file_name)
                )
        except ClientError as e:
            logging.error(e)
            return False
        return {object_name: "Uploaded"}

    async def download_file(self, bucket_name: str, file_name: Path, object_name: str, extra_args: dict=None):
        """[Download file from Bucket]

        Args:
            bucket_name (str): [Name of bucket to download from.]
            file_name (Path): [file_name is used to write bytes of object downloaded from bucket]
            object_name (str): [real object name located in bucket].
            extra_args (dict, optional): [description]. Defaults to None.
        """
        __s3_bucket = self.s3_resource.Bucket(bucket_name)
        
        try:
            with open(file_name, 'wb') as f:
                __s3_bucket.download_file(
                    file_name,
                    object_name
                )
                # self.s3_client.download_fileobj(bucket_name, object_name, f)
        except Exception as err:
            logging.error(err)
            return str(err)
        return {object_name: "Downloaded"}
        

    async def list_buckets(self):
        """[List existing buckets]

        Returns:
            [dict]: [List of buckets]
        """
        buckets = []
        for bucket in self.s3_resource.buckets.all():
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
        # s3_resource = self.session.resource("s3")
        try:
            if self.region is None:
                self.s3_resource.create_bucket(Bucket=bucket_name)
            else:
                location = {'LocationConstraint': self.region}

                self.s3_resource.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration=location
                    )

        except ClientError as e:
            logging.error(e)
            return False
        return True


    async def list_objects(self, bucket_name, prefix: str=None):
        """[List objects in Bucket]

        Args:
            bucket_name ([str]): [Name of Bucket]
            prefix (str, optional): [Prefix parameter used to filter the paginated results by prefix server-side before sending them to the client]. Defaults to None.

        Returns:
            [Iterator]: [PageIterator]
        """

        operation_parameters = {"Bucket": bucket_name}

        if prefix:
            operation_parameters = operation_parameters["Prefix"] =  prefix

        paginator = self.s3_client.get_paginator('list_objects')

        page_iterator = paginator.paginate(**operation_parameters)

        return page_iterator


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