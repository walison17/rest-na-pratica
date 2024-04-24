import boto3
from botocore.client import Config
from django.conf import settings


def create_presigned_url(
    bucket_name,
    object_key,
    content_type,
    expiration=3600,
):
    s3_client = boto3.client(
        "s3",
        endpoint_url=settings.R2_ENDPOINT_URL,
        config=Config(signature_version="v4"),
    )
    response = s3_client.generate_presigned_url(
        "put_object",
        Params={
            "Bucket": bucket_name,
            "Key": object_key,
            "ContentType": content_type,
        },
        ExpiresIn=expiration,
    )

    return response


def get_presigned_url(
    bucket_name,
    object_key,
    expiration=3600,
):
    s3_client = boto3.client(
        "s3",
        endpoint_url=settings.R2_ENDPOINT_URL,
        config=Config(signature_version="v4"),
    )
    response = s3_client.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": bucket_name,
            "Key": object_key,
        },
        ExpiresIn=expiration,
    )

    return response
