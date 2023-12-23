import boto3
from datetime import datetime, timedelta
def lambda_handler(event, context):
    # Create a CloudWatch client
    cloudwatch = boto3.client('cloudwatch')
   
    # Create an RDS client
    rds = boto3.client('rds')
    #create insight client
    client = boto3.client('pi')
    # Calculate start and end times
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=14) 
    # Get a list of all RDS instances
    response = rds.describe_db_instances()
    instances = response['DBInstances']
    print(instances)
    #Loop through each RDS instance
    # Loop through each RDS instance
    for instance in instances:
        #verify if insights are enabled if not it enables the insights
        if instance["PerformanceInsightsEnabled"]!=True:
            #enabling insights 
            rds_client.modify_db_instance(
                DBInstanceIdentifier=instance["DBInstanceIdentifier"],
                EnablePerformanceInsights=True,
                PerformanceInsightsRetentionPeriod=7  # Set the retention period as needed
            )
    
            # Wait for the modification to complete (optional)
            rds_client.get_waiter('db_instance_modified').wait(
                DBInstanceIdentifier=instance["DBInstanceIdentifier"],
            )
        else:
            pass
        rds_instance_id = instance['DbiResourceId']
        print(rds_instance_id)
        # Get the RDS Performance Insights metrics
        response = client.get_resource_metrics(
            ServiceType='RDS',
            Identifier=rds_instance_id,
            MetricQueries=[
                {
                    'Metric': 'db.load.avg',
                },
            ],
            StartTime=start_time,
            EndTime=end_time,
            PeriodInSeconds=1,
            MaxResults=100,
            PeriodAlignment='END_TIME'
        )
        print(response)

        metric_data = response['MetricList'][0]
        metric_name = f"{metric_data['Key']['Metric']}_{response['Identifier']}"
        
        # Prepare CloudWatch MetricData
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
        
        # Put metric data to CloudWatch
        cloudwatch.put_metric_data(
            Namespace='RDS/PerformanceInsights',
            MetricData=cloudwatch_metric_data
        )
    return {
        'statusCode': 200,
        'body': 'Metrics exported successfully for all RDS instances'
    }
