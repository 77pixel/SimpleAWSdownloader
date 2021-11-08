#Simple AWS bucket files synchro with local folder

import boto3
from boto3.session import Session
from botocore.config import Config
import os

BUCKET_NAME = 'BUCKET_NAME'
PREFIX = 'PREFIX/'

boto3.set_stream_logger('')

s3 = boto3.client('s3', aws_access_key_id="YOUR_KEY", aws_secret_access_key="SECRET_KEY")
paginator = s3.get_paginator('list_objects_v2')
pages = paginator.paginate(Bucket= BUCKET_NAME, Prefix= PREFIX)

vol_sum = 0

for page in pages:    
    for obj in page['Contents']:
        file = obj['Key']
        flie_name = os.path.basename(file)
        file_path = os.path.dirname(file)
        vol_sum += obj['Size']
        try:
            s3.download_file(BUCKET_NAME, file, file)
        except: 
            if not os.path.exists(file_path):
                os.makedirs(file_path)
                s3.download_file(BUCKET_NAME, file, file)

print (vol_sum /1024 / 1024 )
