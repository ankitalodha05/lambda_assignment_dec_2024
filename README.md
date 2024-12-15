# Assignment 1:
Automated Instance Management Using AWS Lambda and Boto3

## Objective
In this assignment, you will gain hands-on experience with AWS Lambda and Boto3, Amazon's SDK for Python. The goal is to create a Lambda function that will automatically manage EC2 instances based on their tags.

## Task
You are tasked with automating the stopping and starting of EC2 instances based on tags.

### Specific Requirements:
1. **Setup**:
   - Create two EC2 instances.
   - Tag one of them as `Auto-Stop` and the other as `Auto-Start`.
2. **Lambda Function Creation**:
   - Set up an AWS Lambda function.
   - Ensure that the Lambda function has the necessary IAM permissions to describe, stop, and start EC2 instances.
3. **Coding**:
   - Using Boto3 in the Lambda function:
     - Detect all EC2 instances with the `Auto-Stop` tag and stop them.
     - Detect all EC2 instances with the `Auto-Start` tag and start them.
4. **Testing**:
   - Manually invoke the Lambda function.
   - Confirm that the instance tagged `Auto-Stop` stops and the one tagged `Auto-Start` starts.

---

## Instructions

### 1. EC2 Setup
1. Navigate to the EC2 dashboard and create two new t2.micro instances (or any other available free-tier type).
2. Tag the instances as follows:
   - First instance:
     - Key: `Action`
     - Value: `Auto-Stop`
   - Second instance:
     - Key: `Action`
     - Value: `Auto-Start`
-![image](https://github.com/user-attachments/assets/5a91852c-1e5f-4bda-9ee8-4f6a85010ce2)


### 2. Lambda IAM Role
1. Go to the IAM dashboard.
2. Create a new role for Lambda.
3. Attach the `AmazonEC2FullAccess` policy to this role.
   - **Note**: In a real-world scenario, limit permissions for better security.
-![image](https://github.com/user-attachments/assets/df9d0577-40ab-4127-bfde-1e0a0dd16aa1)


### 3. Lambda Function
1. Navigate to the Lambda dashboard and create a new function.
2. Choose Python 3.x as the runtime.
3. Assign the IAM role created in the previous step.
4. Write the Boto3 Python script:
   - Initialize a boto3 EC2 client.
   - Describe instances with `Auto-Stop` and `Auto-Start` tags.
   - Stop the `Auto-Stop` instances and start the `Auto-Start` instances.
   - Print the affected instance IDs for logging purposes.
-
#### Example Code
```python
import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')

    # Describe instances with the 'Action' tag
    response = ec2.describe_instances(
        Filters=[
            {'Name': 'tag:Action', 'Values': ['Auto-Stop', 'Auto-Start']},
            {'Name': 'instance-state-name', 'Values': ['running', 'stopped']}
        ]
    )

    auto_stop_instances = []
    auto_start_instances = []

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            for tag in instance.get('Tags', []):
                if tag['Key'] == 'Action':
                    if tag['Value'] == 'Auto-Stop' and instance['State']['Name'] == 'running':
                        auto_stop_instances.append(instance['InstanceId'])
                    elif tag['Value'] == 'Auto-Start' and instance['State']['Name'] == 'stopped':
                        auto_start_instances.append(instance['InstanceId'])

    # Stop instances
    if auto_stop_instances:
        print(f"Stopping instances: {auto_stop_instances}")
        ec2.stop_instances(InstanceIds=auto_stop_instances)

    # Start instances
    if auto_start_instances:
        print(f"Starting instances: {auto_start_instances}")
        ec2.start_instances(InstanceIds=auto_start_instances)

    return {
        'statusCode': 200,
        'body': f"Stopped instances: {auto_stop_instances}, Started instances: {auto_start_instances}"
    }
```

### 4. Manual Invocation
1. Save the Lambda function.
2. Test it by manually invoking it from the AWS Lambda console.
3. Go to the EC2 dashboard and confirm:
   - Instances tagged `Auto-Stop` should stop.
   - Instances tagged `Auto-Start` should start.

----------------------------------------------------------------------------------------------
