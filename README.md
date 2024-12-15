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


# Assignment 15:

Implement a Log Cleaner for S3

## Objective
Create a Lambda function that automatically deletes logs in a specified S3 bucket that are older than 90 days.

---

## Instructions

### Step 1: Create an S3 Bucket
1. **Log in to the AWS Management Console**.
2. **Navigate to the S3 service**.
3. Click **'Create bucket'**:
   - Enter a bucket name (e.g., `log-cleaner-bucket`).
   - Choose a region.
   - Leave other settings as default for simplicity.
4. Click **'Create bucket'**.
5. Test this Lambda function with 1-day-old logs. If it works for 1-day-old logs, it will work for 90-day-old logs also.
6. I have uploaded a file name ankita.txt in my log_cleaner_bucket.I will test it after 24 hours(1 day).

-![image](https://github.com/user-attachments/assets/aa566cd8-1c78-40f2-8915-93c37386c9a2)


### Step 2: Create an IAM Role
1. **Navigate to the IAM service**.
2. Click **'Roles'** > **'Create role'**.
3. Choose **'AWS Service'** > **'Lambda'** > Click **'Next'**.
4. Attach the following managed policy:
   - `AmazonS3FullAccess` (for simplicity; in production, restrict permissions).
5. Name the role (e.g., `LogCleanerLambdaRole`) and create the role.

-![image](https://github.com/user-attachments/assets/e8b23873-1e89-4651-bb94-50892298e913)


### Step 3: Create a Lambda Function
1. **Navigate to the Lambda service**.
2. Click **'Create function'**:
   - **Function name**: `LogCleanerFunction`.
   - **Runtime**: `Python 3.x`.
   - **Execution role**: Choose **'Use an existing role'** and select the role created in Step 2.
3. Click **'Create function'**.

![image](https://github.com/user-attachments/assets/04eb5f62-ea53-4ae8-9215-117157a29b7b)


### Step 4: Add Environment Variables
1. Open your Lambda function.
2. Scroll down to the **'Environment variables'** section and click **'Edit'**.
3. Add the following environment variable:
   - **Key**: `BUCKET_NAME`
   - **Value**: Name of your S3 bucket (e.g., `log-cleaner-bucket`).
  
-![image](https://github.com/user-attachments/assets/780d5c3f-89d9-4bf9-8712-124baa38c21c)


### Step 5: Write the Lambda Function Code
1. In the Lambda function, scroll to the **'Code source'** section.
2. Replace the existing code with the following:

```python
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
```

3. Click **'Deploy'**.

-![image](https://github.com/user-attachments/assets/6cdaf4aa-76f3-4577-b3b8-01eb303c8083)

In the given screenshot- i have tested this code with 1 day older logs.

### Step 6: Test the Lambda Function
1. Click **'Test'** and create a new test event:
   - **Event template**: `Hello World`.
   - **Name**: `TestEvent`.
   - **Payload**: `{}`.
2. Click **'Test'** to run the function.
-![image](https://github.com/user-attachments/assets/44de3988-595c-4383-87f1-e7d5b84a16ce)

3. Check the logs in **'Amazon CloudWatch Logs'** to verify that logs older than 1 day are being deleted.
-![image](https://github.com/user-attachments/assets/93b66c1a-279f-4c8f-be50-0012d2131a91)

4. It is working fine on 1 day old logs , So we can change our code accordingly, If we want to delete logs older then 90 days, mention it in code.



### Step 7: Schedule the Lambda Function
1. **Navigate to Amazon EventBridge**.
-![image](https://github.com/user-attachments/assets/068ec99d-5d84-4de3-bfea-5eb57a43074b)


3. Click **'Create rule'**:
   - **Name**: `WeeklyLogCleaner`.
   - **Event Source**: `Schedule`.
   - **Schedule Expression**: `cron(0 0 ? * 1 *)` (Runs every Monday at midnight UTC).
4. Under **'Targets'**, select **'Lambda function'**.
5. Choose the Lambda function (`LogCleanerFunction`) and click **'Create`**.
![image](https://github.com/user-attachments/assets/10bbd4cf-b8a6-4f48-a655-3169a29eb974)


---

## Summary
This document outlines the steps to create and schedule a Lambda function to automatically delete logs older than 90 days in a specified S3 bucket. By following the above steps, you will have an automated process to manage log retention in your S3 bucket.

----------------------------------------------------------------------------------------------------------

# Assignment 14:
Monitor EC2 Instance State Changes Using AWS Lambda, Boto3, and SNS

## Objective
Implement a system to monitor EC2 instance state changes and send notifications via SNS when instances are started or stopped.

## Steps

### Step 1: Set Up SNS
1. Create a new SNS topic in the AWS Management Console.
2. Subscribe your email to the topic and confirm the subscription.

### Step 2: Create an IAM Role for Lambda
1. Create a role with permissions for EC2 state monitoring and SNS publishing.
2. Attach `AmazonEC2ReadOnlyAccess` and `AmazonSNSFullAccess` policies or a custom policy.

### Step 3: Develop the Lambda Function
1. Create a Lambda function with Python 3.x runtime.
2. Assign the IAM role created earlier.
3. Use the following code to handle EC2 state change events:

    ```python
    import json
    import boto3

    def lambda_handler(event, context):
        sns_client = boto3.client('sns')
        sns_topic_arn = '<YOUR_SNS_TOPIC_ARN>'

        detail = event['detail']
        instance_id = detail['instance-id']
        state = detail['state']

        message = f"EC2 Instance {instance_id} is now {state}."
        sns_client.publish(TopicArn=sns_topic_arn, Message=message, Subject='EC2 State Change Notification')
    ```
4. Replace `<YOUR_SNS_TOPIC_ARN>` with your SNS topic ARN and deploy the function.

### Step 4: Configure EventBridge
1. Create an EventBridge rule to trigger the Lambda function on EC2 state changes.
2. Set the event source to `AWS services > EC2` and select `EC2 Instance State-change Notification`.
3. Add the Lambda function as the target.

### Step 5: Test the Setup
1. Start or stop an EC2 instance.
2. Verify that you receive an email notification about the state change.

### Troubleshooting
- **No Notifications**: Ensure the email subscription is confirmed and permissions are correctly set.
- **Lambda Errors**: Verify the SNS topic ARN and Lambda IAM permissions.
- **EventBridge Issues**: Check if the rule is active and properly configured.

### Cleanup (Optional)
1. Delete the Lambda function, EventBridge rule, and SNS topic if no longer needed.
2. Remove the IAM role if it is no longer required.
