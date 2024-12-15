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
-![image](https://github.com/user-attachments/assets/16db616e-3024-4610-ab2d-48e7ede2b8ff)

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

-![image](https://github.com/user-attachments/assets/36660d15-cea3-4056-b2c2-837ce49d5ac1)

-![image](https://github.com/user-attachments/assets/e69eff51-2949-4f8b-8a9d-eaba64d20461)

-![image](https://github.com/user-attachments/assets/e2a33e6f-e338-4a0c-9b86-003dc771c183)

-![image](https://github.com/user-attachments/assets/6da5a58d-e84e-4e2b-b571-4fe061e09dda)

## Deliverables
1. A screenshot of the EC2 instances before and after Lambda execution, showing their states.
2. The Python code of the Lambda function.
3. A brief report summarizing the steps taken and any challenges faced during the assignment.

---

## Notes
- Use the AWS free-tier resources to avoid incurring costs.
- Ensure the IAM role for Lambda has the required permissions for the described tasks.
- Validate the tags properly before performing actions to avoid unintended behavior.

---

## Conclusion
This assignment provided hands-on experience with AWS Lambda and Boto3, demonstrating the power of automation in managing AWS resources. By successfully completing the task, you learned how to:
1. Use AWS tags to categorize and manage EC2 instances.
2. Write Python scripts leveraging Boto3 to perform operations on EC2 instances.
3. Configure IAM roles and policies to enable secure interactions between Lambda and AWS services.

The assignment highlights the importance of automation in cloud environments, helping streamline operational tasks, improve efficiency, and reduce human error.





----------------------------------------------------------------------------------------------
