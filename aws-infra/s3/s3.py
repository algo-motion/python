"""Create an S3 bucket in the region from config.json and wait until it exists.

COST WARNING: an empty bucket is free, but storing objects and making
requests are billed once usage goes beyond the AWS Free Tier.
Delete the bucket when you finish the lab.
"""

import argparse
import json
import sys
from pathlib import Path

import boto3
from botocore.exceptions import ClientError

# config.json lives at the repo root: aws-infra/s3/s3.py -> ../../config.json
CONFIG_PATH = Path(__file__).resolve().parents[2] / "config.json"


def load_region(config_path=CONFIG_PATH):
    """Return the default AWS region defined in config.json."""
    config = json.loads(Path(config_path).read_text(encoding="utf-8"))
    return config["region"]


def create_bucket(client, bucket_name, region):
    """Create a bucket and wait until it exists.

    Returns True if the bucket was created, False if we already own it.
    Raises ClientError for any other failure (e.g. name taken by another account).
    """
    params = {"Bucket": bucket_name}
    # us-east-1 is the default location and rejects an explicit LocationConstraint
    if region != "us-east-1":
        params["CreateBucketConfiguration"] = {"LocationConstraint": region}

    try:
        client.create_bucket(**params)
    except ClientError as error:
        # Bucket names are global; re-running the script hits this code
        if error.response["Error"]["Code"] == "BucketAlreadyOwnedByYou":
            return False
        raise

    waiter = client.get_waiter("bucket_exists")
    waiter.wait(Bucket=bucket_name, WaiterConfig={"Delay": 2, "MaxAttempts": 10})
    return True


def main():
    default_region = load_region()
    parser = argparse.ArgumentParser(description="Create an S3 bucket")
    parser.add_argument("bucket", help="globally unique bucket name")
    parser.add_argument(
        "--region",
        default=default_region,
        help=f"AWS region (default: {default_region} from {CONFIG_PATH.name})",
    )
    args = parser.parse_args()

    client = boto3.client("s3", region_name=args.region)
    try:
        created = create_bucket(client, args.bucket, args.region)
    except ClientError as error:
        print(f"Failed to create bucket {args.bucket}: {error}", file=sys.stderr)
        return 1

    if created:
        print(f"Bucket {args.bucket} is created in {args.region}")
    else:
        print(f"Bucket {args.bucket} already exists in your account")
    return 0


if __name__ == "__main__":
    sys.exit(main())
