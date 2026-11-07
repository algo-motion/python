"""Unit tests for s3.py. They use botocore's Stubber, so no real AWS call is made."""

import json
import tempfile
import unittest
from pathlib import Path

import boto3
from botocore.exceptions import ClientError
from botocore.stub import Stubber

import s3

# The bucket_exists waiter checks the HTTP status code, which Stubber leaves empty by default
HEAD_BUCKET_OK = {"ResponseMetadata": {"HTTPStatusCode": 200}}


def make_client(region):
    # Dummy credentials: Stubber answers every call, nothing reaches AWS
    return boto3.client(
        "s3",
        region_name=region,
        aws_access_key_id="testing",
        aws_secret_access_key="testing",
    )


class LoadRegionTest(unittest.TestCase):
    def test_reads_region_from_config(self):
        with tempfile.TemporaryDirectory() as tmp:
            config_path = Path(tmp) / "config.json"
            config_path.write_text(json.dumps({"region": "eu-west-1"}), encoding="utf-8")
            self.assertEqual(s3.load_region(config_path), "eu-west-1")


class CreateBucketTest(unittest.TestCase):
    def test_creates_bucket_with_location_constraint(self):
        client = make_client("ap-northeast-1")
        with Stubber(client) as stubber:
            stubber.add_response(
                "create_bucket",
                {},
                {
                    "Bucket": "my-bucket",
                    "CreateBucketConfiguration": {"LocationConstraint": "ap-northeast-1"},
                },
            )
            # The bucket_exists waiter polls HeadBucket
            stubber.add_response("head_bucket", HEAD_BUCKET_OK, {"Bucket": "my-bucket"})

            self.assertTrue(s3.create_bucket(client, "my-bucket", "ap-northeast-1"))
            stubber.assert_no_pending_responses()

    def test_us_east_1_omits_location_constraint(self):
        client = make_client("us-east-1")
        with Stubber(client) as stubber:
            stubber.add_response("create_bucket", {}, {"Bucket": "my-bucket"})
            stubber.add_response("head_bucket", HEAD_BUCKET_OK, {"Bucket": "my-bucket"})

            self.assertTrue(s3.create_bucket(client, "my-bucket", "us-east-1"))
            stubber.assert_no_pending_responses()

    def test_bucket_already_owned_returns_false(self):
        client = make_client("ap-northeast-1")
        with Stubber(client) as stubber:
            stubber.add_client_error("create_bucket", service_error_code="BucketAlreadyOwnedByYou")

            self.assertFalse(s3.create_bucket(client, "my-bucket", "ap-northeast-1"))

    def test_bucket_owned_by_someone_else_raises(self):
        client = make_client("ap-northeast-1")
        with Stubber(client) as stubber:
            stubber.add_client_error("create_bucket", service_error_code="BucketAlreadyExists")

            with self.assertRaises(ClientError):
                s3.create_bucket(client, "my-bucket", "ap-northeast-1")


if __name__ == "__main__":
    unittest.main()
