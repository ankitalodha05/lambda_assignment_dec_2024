    # Extract details from the event
    detail = event.get('detail', {})
    instance_id = detail.get('instance-id', 'Unknown')
    state = detail.get('state', 'Unknown')

    # Prepare the message
    message = f"EC2 Instance {instance_id} is now {state}."
    print(message)

    # Publish the message to SNS
    sns_client = boto3.client('sns')
    sns_topic_arn = 'arn:aws:sns:us-east-1:225989348530:EC2StateChangeTopic'
    response = sns_client.publish(
        TopicArn=sns_topic_arn,
        Message=message,
        Subject='EC2 State Change Notification'
    )
    print("SNS Response:", response)

except Exception as e:
    print("Error:", str(e))
    raise
```
