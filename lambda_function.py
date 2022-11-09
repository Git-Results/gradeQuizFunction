import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
  
  #UPDATED
  #Create string from JSON then convert to dict
  print(event)
  jsonEvent = json.dumps(event)
  eventBody = event['body']
  answersRecieved = json.loads(eventBody)
  
  #Table information
  client = boto3.resource('dynamodb', region_name='us-east-1')
  table = client.Table('gitCCP_quiz')   

  answersCorrect = {}
  i = 1
  score = 0
    
  while i < 11:
    
    iString = str(i)
    item = table.get_item(Key={
    'question_id': str(iString),
    })
    
    print(item)
    
    correctAnswer = str(item['Item']['correct_answer'])
    dataHeader = (f'question{iString}Answer')
    answerRecieved = answersRecieved[f'question{iString}Answer']
    
    print(answerRecieved)
      
    print('The correct answer is: ' + correctAnswer)
    if answerRecieved == correctAnswer:
      print("True")
      score = score + 10
      answersCorrect.update({dataHeader: True})
    else:
      print("False")
      answersCorrect.update({dataHeader: False})
      
    i = i + 1
    
  print(answersCorrect)
  print(score)

  return {
    'isBase64Encoded': False,
    'headers': { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': 'http://my-static-bucket-jenkins.s3-website-us-east-1.amazonaws.com' },
    'statusCode': 200,
    'body': json.dumps({'answersCorrect': answersCorrect, 'score': score})
  }
