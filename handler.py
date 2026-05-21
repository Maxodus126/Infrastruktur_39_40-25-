import json
import boto3
import os

dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url=os.environ.get('DYNAMODB_ENDPOINT', 'http://localhost:4566'),
    region_name='us-east-1',
    aws_access_key_id='test',
    aws_secret_access_key='test'
)

def lambda_handler(event, context):
    """
    GET /students
    Mengembalikan semua item dari DynamoDB tabel 'mahasiswa'
    """
    try:
        table = dynamodb.Table('mahasiswa')

        # Scan semua item dari tabel mahasiswa
        response = table.scan()
        items = response.get('Items', [])

        # Handle pagination jika data banyak
        while 'LastEvaluatedKey' in response:
            response = table.scan(
                ExclusiveStartKey=response['LastEvaluatedKey']
            )
            items.extend(response.get('Items', []))

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'students': items,
                'count': len(items),
                'message': 'OK'
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'error': str(e),
                'message': 'Internal server error'
            })
        }
