"""
AWS VPC read-only tools.

These tools will be used by the agent to inspect
AWS networking infrastructure.
"""

import boto3


def describe_vpcs(region):
    """
    Retrieve VPC information from AWS.

    This is a READ operation.
    It does not modify AWS infrastructure.
    """

    ec2 = boto3.client(
        "ec2",
        region_name=region
    )

    response = ec2.describe_vpcs()

    return response["Vpcs"]


if __name__ == "__main__":
    region = "us-east-1"

    vpcs = describe_vpcs(region)

    for vpc in vpcs:
        print(vpc)
