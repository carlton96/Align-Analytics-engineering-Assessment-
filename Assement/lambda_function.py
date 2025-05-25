import json
import boto3
import pandas as pd
import io
import logging

s3 = boto3.client('s3')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        # 1. Validate and parse S3 trigger info
        if 'Records' not in event or len(event['Records']) == 0:
            logger.error("Event missing 'Records' key or it's empty.")
            return {"statusCode": 400, "body": "Invalid event: No Records found"}

        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']

        logger.info(f"Processing file from bucket: {bucket}, key: {key}")

        if not key.endswith('.parquet'):
            logger.warning(f"File '{key}' skipped (not a .parquet file).")
            return {"statusCode": 200, "body": f"Skipped: {key} is not a .parquet file"}

        # 2. Read the Parquet file from S3
        try:
            response = s3.get_object(Bucket=bucket, Key=key)
            parquet_data = response['Body'].read()
            df = pd.read_parquet(io.BytesIO(parquet_data))
            logger.info("Parquet file successfully read into DataFrame.")
        except Exception as e:
            logger.error(f"Failed to read or parse Parquet file: {e}")
            return {"statusCode": 500, "body": "Error reading Parquet file"}

        # 3. Convert to CSV
        try:
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)
            logger.info("DataFrame successfully converted to CSV.")
        except Exception as e:
            logger.error(f"CSV conversion failed: {e}")
            return {"statusCode": 500, "body": "Error converting to CSV"}

        # 4. Define destination key
        dest_key = key.replace('.parquet', '.csv')

        # 5. Upload to processed-bucket
        try:
            s3.put_object(
                Bucket='processed-bucket-analytics-v1',
                Key=dest_key,
                Body=csv_buffer.getvalue()
            )
            logger.info(f"CSV file uploaded to processed-bucket-analytics-v1/{dest_key}")
        except Exception as e:
            logger.error(f"Failed to upload CSV to destination bucket: {e}")
            return {"statusCode": 500, "body": "Error uploading CSV to destination bucket"}

        return {
            'statusCode': 200,
            'body': json.dumps(f"File converted and saved to processed-bucket-analytics-v1/{dest_key}")
        }

    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps("An unexpected error occurred.")
        }
