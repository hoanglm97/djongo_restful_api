import boto3


s3 = boto3.resource('s3', endpoint_url='https://ss-hn-1.vccloud.vn',
    aws_access_key_id = '56YUI4XURX8MHBRMUPNN',
    aws_secret_access_key = 'eihKLE5RDhXeIeJFuYVz5JTaWQiw7Ghs92SAaCYf') 


for bucket in s3.buckets.all():
    print(bucket.name)
 

s3.create_bucket(Bucket='bucket-04')
