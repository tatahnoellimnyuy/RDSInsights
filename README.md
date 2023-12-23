# AWS Lambda Function Documentation

## Overview

This AWS Lambda function automates the collection and export of RDS (Relational Database Service) Performance Insights metrics to CloudWatch. The function is designed to run periodically using a CloudWatch Events rule. The following are the key steps of the function:

1. **Enable Performance Insights:** Checks if Performance Insights is enabled for each RDS instance. If not, it enables Performance Insights with a specified retention period.

2. **Retrieve Performance Insights Metrics:** Retrieves the 'db.load.avg' metric for each RDS instance using the AWS RDS Performance Insights API.

3. **Export Metrics to CloudWatch:** Prepares the retrieved metrics and exports them to CloudWatch under the namespace 'RDS/PerformanceInsights' with the appropriate dimensions.

## Function Flow

### Import Required Libraries
```python
import boto3
from datetime import datetime, timedelta
```

### Lambda Handler
```python
def lambda_handler(event, context):
    # Function code here
```

### Initialize Clients
```python
    cloudwatch = boto3.client('cloudwatch')
    rds = boto3.client('rds')
    client = boto3.client('pi')
```

### Set Time Range
```python
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=14)
```

### Retrieve RDS Instances
```python
    response = rds.describe_db_instances()
    instances = response['DBInstances']
```

### Loop Through RDS Instances
```python
    for instance in instances:
        # Function code for each instance
```

### Prepare CloudWatch Metric Data
```python
        cloudwatch_metric_data = [
            {
                'MetricName': metric_name,
                'Dimensions': [
                    {
                        'Name': 'DBInstanceIdentifier',
                        'Value': rds_instance_id
                    }
                ],
                'Timestamp': data_point['Timestamp'],
                'Value': data_point['Value'],
                'Unit': 'None'  # Replace 'None' with the appropriate unit for your metric
            }
            for data_point in metric_data['DataPoints']
        ]
```

### Export Metrics to CloudWatch
```python
        cloudwatch.put_metric_data(
            Namespace='RDS/PerformanceInsights',
            MetricData=cloudwatch_metric_data
        )
```

### Return Response
```python
    return {
        'statusCode': 200,
        'body': 'Metrics exported successfully for all RDS instances'
    }
```

## Input Parameters

- **Event:** The input event received by the Lambda function (not used in the current implementation).
- **Context:** The execution context for the Lambda function (not used in the current implementation).

## Output

The function returns a JSON response indicating the success of the metric export.

## Prerequisites

- **IAM Role Permissions:** The Lambda function requires an IAM role with the following permissions:
  - `rds:FullAcess`
  - `cloudwatch:FullAccess`

## CloudWatch Event

To schedule the Lambda function, set up a CloudWatch Events rule with a desired schedule expression (e.g., cron expression).

## Considerations



- The default data collection period is set to the last 14 days. You can adjust this period by modifying the `timedelta` value in the `start_time` calculation.

- The CloudWatch namespace used is 'RDS/PerformanceInsights'. Ensure that this namespace aligns with your CloudWatch metric organization.

- The unit for the exported metric is set to 'None'. Modify the 'Unit' field in the CloudWatch MetricData preparation section according to the appropriate unit for your metric.

## Conclusion

This Lambda function streamlines the process of collecting and exporting RDS Performance Insights metrics to CloudWatch, enhancing centralized monitoring and analysis capabilities.