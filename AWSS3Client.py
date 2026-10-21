import boto3

client = boto3.client("s3", region_name="ap-northeast-1")
result = client.list_buckets()

for bucket in result["Buckets"]:
    print(bucket["Name"])