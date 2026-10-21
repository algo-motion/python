import argparse
import json
from pathlib import Path

import boto3

CONFIG_PATH = Path(__file__).with_name("config.json")
config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))

parser = argparse.ArgumentParser(description="List S3 buckets")
parser.add_argument(
    "--region",
    default=config["region"],
    help=f"AWS region (default: {config['region']} from {CONFIG_PATH.name})",
)
args = parser.parse_args()

client = boto3.client("s3", region_name=args.region)
result = client.list_buckets()

for bucket in result["Buckets"]:
    print(bucket["Name"])
