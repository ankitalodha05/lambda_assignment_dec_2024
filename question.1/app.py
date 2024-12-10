
import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    action_tag_key = 'Action'
    
    # Fetch all instances
    instances = ec2.describe_instances(Filters=[{'Name': f'tag:{action_tag_key}', 'Values': ['Auto-Stop', 'Auto-Start']}])
    
    auto_stop_instances = []
    auto_start_instances = []
    
    # Iterate through the instances
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            for tag in instance.get('Tags', []):
                if tag['Key'] == action_tag_key:
                    if tag['Value'] == 'Auto-Stop':
                        auto_stop_instances.append(instance['InstanceId'])
                    elif tag['Value'] == 'Auto-Start':
                        auto_start_instances.append(instance['InstanceId'])
    
    # Stop instances with Auto-Stop tag
    if auto_stop_instances:
        ec2.stop_instances(InstanceIds=auto_stop_instances)
        print(f"Stopped instances: {auto_stop_instances}")
    
    # Start instances with Auto-Start tag
    if auto_start_instances:
        ec2.start_instances(InstanceIds=auto_start_instances)
        print(f"Started instances: {auto_start_instances}")
    
    return {
        'statusCode': 200,
        'body': f"Auto-Stop: {auto_stop_instances}, Auto-Start: {auto_start_instances}"
    }
