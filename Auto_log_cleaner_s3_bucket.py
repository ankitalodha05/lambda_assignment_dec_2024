import boto3
import os
from datetime import datetime, timezone, timedelta

def lambda_handler(event, context):
    # Get the bucket name from environment variable
    bucket_name = os.environ['BUCKET_NAME']
    days_to_keep = 90  # Number of days to retain logs

    # Initialize S3 client
    s3_client = boto3.client('s3')
    bucket_objects = s3_client.list_objects_v2(Bucket=bucket_name)

    if 'Contents' not in bucket_objects:
        return {"status": "No logs found to clean"}

    # Calculate the cutoff date
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_to_keep)

    # Iterate over objects and delete if older than cutoff date
    deleted_count = 0
    for obj in bucket_objects['Contents']:
        last_modified = obj['LastModified']
        if last_modified < cutoff_date:
            s3_client.delete_object(Bucket=bucket_name, Key=obj['Key'])
            deleted_count += 1

    return {
        "status": "Log cleaning completed",
        "deleted_logs_count": deleted_count
    }
