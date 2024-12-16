import boto3
import json
from datetime import datetime

# Helper function to convert datetime to string
def json_serial(obj):
    """JSON serializer for objects not serializable by default"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))  # Log the incoming event
    
    try:
        # Validate event structure
        if 'detail' not in event or 'instance-id' not in event['detail']:
            print("Invalid event structure. 'detail' or 'instance-id' not found.")
            return {
                "statusCode": 400,
                "body": json.dumps("Invalid event structure")
            }
        
        # Extract instance ID and state
        instance_id = event['detail']['instance-id']
        state = event['detail']['state']
        print(f"Instance ID: {instance_id}, State: {state}")
        
        # Only process if the state is 'shutting-down' or 'terminated'
        if state not in ['shutting-down', 'terminated']:
            print(f"Instance {instance_id} is in state '{state}', skipping processing.")
            return {
                "statusCode": 200,
                "body": json.dumps(f"Instance {instance_id} is in state '{state}', no action taken.")
            }
        
        # Initialize AWS clients
        ec2_client = boto3.client('ec2')
        s3_client = boto3.client('s3')
        bucket_name = 'ec2-instance-state-backup'

        # Get instance details
        response = ec2_client.describe_instances(InstanceIds=[instance_id])
        instance_state = response['Reservations'][0]['Instances'][0]
        print(f"Instance state: {json.dumps(instance_state, indent=4, default=json_serial)}")
        
        # Save instance state to S3
        s3_key = f"{instance_id}-{state}.json"
        s3_client.put_object(
            Bucket=bucket_name,
            Key=s3_key,
            Body=json.dumps(instance_state, indent=4, default=json_serial)
        )
        print(f"Successfully saved instance state to S3: {bucket_name}/{s3_key}")
        
        return {
            "statusCode": 200,
            "body": json.dumps(f"State saved for instance {instance_id}")
        }

    except Exception as e:
        print(f"Error: {str(e)}")  # Log any unexpected errors
        return {
            "statusCode": 500,
            "body": json.dumps(f"Error: {str(e)}")
        }
