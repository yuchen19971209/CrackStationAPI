import json
import boto3
import os

s3_client = boto3.client("s3")


def lambda_handler(event, context):

    sha = event["pathParameters"]["shaHash"]

    returnString = ""
    
    sql_exp = ("SELECT s.\"Password\"" 
          "FROM s3object s " 
          "WHERE s.\"ShaHash\"='%s'"%(sha))
    
    response = s3_client.select_object_content(
        Bucket = "mycrackstationyuchen",
        Key = "LookUpTable.csv",
        ExpressionType = 'SQL',
        Expression = sql_exp,
        InputSerialization = {'CSV': {"FileHeaderInfo": "Use"}},
        OutputSerialization = {'CSV': {}},
    )
    
    #  upack query response
    records = []
    for event in response['Payload']:
        if 'Records' in event:
            records.append(event['Records']['Payload'])  
    
    #  store unpacked data as a CSV format
    file_str = ''.join(req.decode('utf-8') for req in records)
    
    #  replace "\n" and "\r"
    file_str = file_str.replace('\n', '').replace('\r', '')
    
    if file_str !="":
        return{
                'statusCode': 200,
                'headers': {
                    "Access-Control-Allow-Headers" : "Content-Type",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                },
                'body': json.dumps({sha:file_str})
        }
    else:
        return {
        'statusCode': 404,
        'headers': {
                    "Access-Control-Allow-Headers" : "Content-Type",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                },
        'body': json.dumps({sha:"Can not find the password in CrackStation"})
        }