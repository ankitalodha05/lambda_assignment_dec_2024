import json
import boto3
import datetime

def lambda_handler(event, context):
    # Initialize EC2 client
    ec2_client = boto3.client('ec2')

    try:
        # Log the incoming event for debugging
        print("Received event:", json.dumps(event, indent=2))

        # Extract the instance ID from the event
        if 'detail' in event and 'instance-id' in event['detail']:
            instance_id = event['detail']['instance-id']
        else:
            raise KeyError("The event does not contain the required 'detail' or 'instance-id' keys.")

        # Get the current date
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')

        # Define the tags
        tags = [
            {'Key': 'LaunchDate', 'Value': current_date},
            {'Key': 'Owner', 'Value': 'AutoTagging'}
        ]

        # Apply tags to the EC2 instance
        response = ec2_client.create_tags(Resources=[instance_id], Tags=tags)

        # Log the success
        print(f"Successfully tagged instance {instance_id} with tags: {tags}")

        return {
            'statusCode': 200,
            'body': f"Tags applied successfully to instance {instance_id}: {tags}"
        }

    except KeyError as e:
        # Handle missing keys in the event
        print(f"KeyError: {str(e)}")
        return {
            'statusCode': 400,
            'body': f"Invalid event structure: {str(e)}"
        }

    except Exception as e:
        # Catch all other exceptions
        print(f"Unexpected error: {str(e)}")
        return {
            'statusCode': 500,
            'body': f"Failed to apply tags: {str(e)}"
        }
