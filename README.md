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
-![image](https://github.com/user-attachments/assets/d500e7fe-856c-463f-ab36-361e6e0a9c6f)

2. Subscribe your email to the topic and confirm the subscription.
-![image](https://github.com/user-attachments/assets/56c84a52-83e5-4d8f-ba7a-c8224fb41a3f)

-![image](https://github.com/user-attachments/assets/ab419c45-0a1f-4b0c-ae5d-282646a5465b)



### Step 2: Create an IAM Role for Lambda
1. Create a role with permissions for EC2 state monitoring and SNS publishing.
-![image](https://github.com/user-attachments/assets/9964186d-7d32-4ea5-9e6f-2946d685b665)

2. Attach `AmazonEC2ReadOnlyAccess` and `AmazonSNSFullAccess` policies and added one custom policy SNSpublish.
-![image](https://github.com/user-attachments/assets/25e073d4-23e5-4206-ba1a-c378cb270aa9)


### Step 3: Develop the Lambda Function
1. Create a Lambda function with Python 3.x runtime.
2. Assign the IAM role created earlier.
-![image](https://github.com/user-attachments/assets/91fa0f14-4574-4cce-9459-6785778e0218)

3. Use the following code to handle EC2 state change events:

    ```python
    import json
import boto3

def lambda_handler(event, context):
    try:
        # Log the event for debugging
        print("Received event:", json.dumps(event, indent=2))

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
5. Replace `<YOUR_SNS_TOPIC_ARN>` with your SNS topic ARN and deploy the function.

### Step 4: Configure EventBridge
1. Create an EventBridge rule to trigger the Lambda function on EC2 state changes.
2. Set the event source to `AWS services > EC2` and select `EC2 Instance State-change Notification`.
-![image](https://github.com/user-attachments/assets/5cd49212-4309-4ec8-8d31-6ca80100a05f)
3. Add the Lambda function as the target.
-![image](https://github.com/user-attachments/assets/681d8b4b-0275-41d6-aef0-e6eff6ea6b2b)


### Step 5: Test the Setup
1. Start or stop an EC2 instance.
-![image](https://github.com/user-attachments/assets/1c9197ef-66c7-430d-91bb-c51175e0ccf2)


3. Verify that you receive an email notification about the state change.
-![image](https://github.com/user-attachments/assets/164e4e54-c1a6-4f96-aff7-a86668a32cb8)


### Troubleshooting
- **No Notifications**: Ensure the email subscription is confirmed and permissions are correctly set.
- **Lambda Errors**: Verify the SNS topic ARN and Lambda IAM permissions.
- **EventBridge Issues**: Check if the rule is active and properly configured.

### Cleanup (Optional)
1. Delete the Lambda function, EventBridge rule, and SNS topic if no longer needed.
2. Remove the IAM role if it is no longer required.

----------------------------------------------------------------------------------
# Assignment 5: Auto-Tagging EC2 Instances on Launch Using AWS Lambda and Boto3

## Objective
Learn to automate the tagging of EC2 instances as soon as they are launched, ensuring better resource tracking and management.

---

## Task
Automatically tag any newly launched EC2 instance with the current date and a custom tag.

---

## Instructions

### 1. EC2 Setup
Ensure you have the capability to launch EC2 instances.

### 2. Lambda IAM Role
1. Navigate to the IAM dashboard and create a new role for Lambda.
-![image](https://github.com/user-attachments/assets/e32b0b0a-ea9d-459a-ae7c-947bf418e746)

3. Attach the `AmazonEC2FullAccess` policy to this role.
4. create an inline policy-
The AllowEC2CreateTags policy allows tagging EC2 instances using ec2:CreateTags for all instances across any region and account. It is used to automate tagging in workflows like Lambda.
![image](https://github.com/user-attachments/assets/9a0b3e57-d036-4338-8fae-a8d0e332cb50)

-

---

### 3. Lambda Function
1. Navigate to the Lambda dashboard and create a new function.
2. Choose Python 3.x as the runtime.
3. Assign the IAM role created in the previous step.
4. Replace the default code with the following:

```python
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
```

5. Deploy the code to save the function.
-![image](https://github.com/user-attachments/assets/74757127-d45f-4263-b0f6-9eed031c6927)


---

### 4. CloudWatch Events
1. Go to the EventBridge Console.

2. Create a New Rule:
    - **Name**: `TagEC2OnLaunch`.
    - **Event Pattern**:
        - **Event source**: AWS services → EC2.
        - **Event type**: EC2 Instance State-change Notification.
        - Add a filter for `state: running` in the Event Pattern section.


3. Final Event Pattern JSON:

```json
{
    "source": ["aws.ec2"],
    "detail-type": ["EC2 Instance State-change Notification"],
    "detail": {
        "state": ["running"]
    }
}
```

4. Set the Target:
    - Attach the Lambda function created earlier (`AutoTagEC2Instance`).

5. Save and enable the rule.
-![image](https://github.com/user-attachments/assets/c44c02d4-c405-4003-9ea6-88111a56ec1a)


---

## Testing

### Manual Test
1. Go to the **Test** tab in Lambda.
2. Use the following test event:

```json
{
    "version": "0",
    "id": "abcd1234-5678-90ab-cdef-EXAMPLE",
    "detail-type": "EC2 Instance State-change Notification",
    "source": "aws.ec2",
    "account": "123456789012",
    "time": "2024-12-14T12:34:56Z",
    "region": "us-east-1",
    "resources": ["arn:aws:ec2:us-east-1:123456789012:instance/i-0bcf4a6cdc4d9fe57"],
    "detail": {
        "instance-id": "i-0bcf4a6cdc4d9fe57",
        "state": "running"
    }
}
```

- Replace `i-0bcf4a6cdc4d9fe57` with a valid instance ID.
- Run the test and confirm tags are applied.

### Dynamic Test
1. Launch a new EC2 instance from the EC2 Dashboard.
2. Check the **Tags** tab for the instance to confirm the tags are applied automatically.
-![image](https://github.com/user-attachments/assets/a72ec2b8-c75b-4146-819f-197d9d4f2cf5)
![image](https://github.com/user-attachments/assets/f5cbd491-b264-4c75-aca9-6735194a4888)



---

## Troubleshooting

### Issue: `KeyError: 'detail'`
- **Cause**: The event structure does not contain the required `detail` or `instance-id` keys.
- **Solution**: Verify the EventBridge rule's event pattern matches the expected format.

### Issue: `InvalidID when calling CreateTags`
- **Cause**: The `instance-id` in the event does not exist in your account.
- **Solution**: Use a valid instance ID and ensure the EC2 instance exists.

### Issue: `UnauthorizedOperation`
- **Cause**: The IAM role lacks sufficient permissions to tag the instance.
- **Solution**: Attach the `AmazonEC2FullAccess` policy or a custom policy with `ec2:CreateTags` permission.

---

## Clean Up Resources

1. **Terminate EC2 Instances**:
    - Go to the EC2 Dashboard → Select and terminate the test instances.

2. **Delete Resources**:
    - Delete the Lambda function.
    - Delete the EventBridge rule.

---

## References

### Boto3 Create Tags Command
```python
response = ec2_client.create_tags(Resources=[instance_id], Tags=tags)
```

### AWS CLI to Tag an Instance Manually
```bash
aws ec2 create-tags --resources i-0bcf4a6cdc4d9fe57 --tags Key=LaunchDate,Value=2024-12-14 Key=Owner,Value=AutoTagging
```

# **ASSIGNMENT 18: AUTOSAVE EC2 INSTANCE STATE BEFORE SHUTDOWN**

### **Objective**
Before an EC2 instance is shut down, automatically save its current state to an S3 bucket.

### **Instructions**
1. **Create a Lambda Function**.
2. Using **Boto3**, the function should:
   - Detect when an EC2 instance is about to be terminated.
   - Save the current state or necessary files from the EC2 instance to an S3 bucket.
3. Use **CloudWatch Events** to trigger this Lambda function whenever an EC2 termination command is detected.

---

# Documentation: Autosave EC2 Instance State Before Shutdown
---
## Objective
The goal of this assignment is to create a process where, before an EC2 instance is shut down or terminated, its current state is automatically saved to an S3 bucket. This document outlines the steps, configuration, and troubleshooting performed to achieve this functionality.
---
## Solution Overview

1. **CloudWatch Rule**: Detect EC2 instance state-change events such as `shutting-down` or `terminated`.
2. **Lambda Function**: Process the events, fetch the EC2 instance details, and store them in an S3 bucket.
3. **S3 Bucket**: Store instance details as JSON files.
4. **IAM Roles and Policies**: Configure permissions for Lambda and S3 access.
5. **Testing and Troubleshooting**: Validate functionality and resolve issues.
---
## Step-by-Step Implementation
-----------------------------------------------------------------------------
### Step 1: Create an S3 Bucket
1. Navigate to the **S3 Console**.
2. Click **"Create Bucket"**.
3. Enter a unique bucket name, such as `ec2-instance-state-backup`.
4. Leave default settings (Block Public Access enabled) and click **"Create Bucket"**.
5. - ![image](https://github.com/user-attachments/assets/70259562-766b-4b71-8a44-db4fdd748e28)

6. Set the bucket policy to allow access from the Lambda function:
   ```json
   {
       "Version": "2012-10-17",
       "Statement": [
           {
               "Effect": "Allow",
               "Principal": {
                   "AWS": "arn:aws:iam::225989348530:role/service-role/AutoTagEC2Instance-role-35hgkdnr"
               },
               "Action": "s3:PutObject",
               "Resource": "arn:aws:s3:::ec2-instance-state-backup/*"
           }
       ]
   }
   ```
----------------------------------------------------- 
### Step 2: Configure IAM Role for Lambda
1. Navigate to the **IAM Console**.
2. Create a role for **AWS Lambda**.
3. Attach the following policies to the role:
   - **AmazonEC2ReadOnlyAccess** (to read instance details).
   - **AmazonS3FullAccess** (or a custom policy with `s3:PutObject` permissions for the S3 bucket).
   - ![image](https://github.com/user-attachments/assets/705bc7c4-0bcb-45e8-97a7-70f3a9470fb8)


   Custom policy for S3:
   ```json
   {
       "Version": "2012-10-17",
       "Statement": [
           {
               "Effect": "Allow",
               "Action": "s3:PutObject",
               "Resource": "arn:aws:s3:::ec2-instance-state-backup/*"
           }
       ]
   }
   ```
   
4. Assign the role to your Lambda function.

### Step 3: Create a CloudWatch Rule
1. Navigate to the **CloudWatch Console**.
2. Go to **Rules** and click **"Create Rule"**.
3. Set the event source:
   - **Service Name**: `EC2`
   - **Event Type**: `EC2 Instance State-change Notification`
   - **Specific State**: `shutting-down`
4. Add the Lambda function as the target.
5. Name the rule `ec2-shutdown-trigger` and enable it.
 - ![image](https://github.com/user-attachments/assets/2ab9b12c-ac57-4cc4-84ba-667ee608ab77)

-

-----------------------------------------
### Step 4: Write the Lambda Function

Deploy the following Python code as your Lambda function:

```python
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
```

------------
### Step 5: Testing
1. **Simulate a Shutdown Event**:
   - Terminate or shut down an EC2 instance.
2. **Validate S3**:
   - Go to the S3 bucket (`ec2-instance-state-backup`) and verify that a file named `<instance-id>-shutting-down.json` or `<instance-id>-terminated.json` is created.
   - ![image](https://github.com/user-attachments/assets/29c45103-55fc-4bb9-b33d-b0538bd9c101)
    - ![image](https://github.com/user-attachments/assets/bc967801-b2a0-4cec-ab0a-aa2ccfdfc436)


------------
### Step 6: Troubleshooting
1. **Error: Object of type datetime is not JSON serializable**:
   - Resolved by adding the `json_serial` helper function to convert `datetime` objects to ISO 8601 string format.
2. **Error: Invalid event structure**:
   - Verified the CloudWatch Rule to ensure it sends the correct payload.
3. **S3 Upload Issues**:
   - Ensured the Lambda role had `s3:PutObject` permissions.
   - Verified the S3 bucket policy was correctly configured.
4. **Manual Testing**:
   - Used a simulated event payload to test the Lambda function in the AWS Console:

     ```json
     {
         "version": "0",
         "id": "cd2d7024-22b4-4a35-91c9-ef5b88b43326",
         "detail-type": "EC2 Instance State-change Notification",
         "source": "aws.ec2",
         "account": "225989348530",
         "time": "2024-12-15T00:12:43Z",
         "region": "us-east-1",
         "resources": ["arn:aws:ec2:us-east-1:225989348530:instance/i-0b48e6081f8209438"],
         "detail": {
           "instance-id": "i-0b48e6081f8209438",
           "state": "shutting-down"
         }
     }
     ```
     
## Conclusion
This solution ensures that EC2 instance details are automatically saved to an S3 bucket before termination or shutdown, providing a reliable backup mechanism. By leveraging AWS services such as CloudWatch, Lambda, and S3, the process is fully automated and scalable.




