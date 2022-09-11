import json

def handler(event, context):
    print(f"Request is {json.dumps(event)}")
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body': 'Helloo, CDK! You have hit {}\n'.format(event['path'])
    }