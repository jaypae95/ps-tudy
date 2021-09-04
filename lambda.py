from settings_local import USERNAME, \
    SLACK_WEBHOOK_URL, \
    SENDER, RECIPIENT, \
    AWS_REGION, \
    AWS_SNS_REGION,\
    AWS_ACCESS_KEY_ID, \
    AWS_SECRET_ACCESS_KEY, \
    PHONENUMBER
import requests
import json
import random
import logging
import boto3
from botocore.exceptions import ClientError


url = 'https://solved.ac/search?query='
for uu in range(len(USERNAME)):
    url += f'-solved_by%3A{USERNAME[uu]}+'
url += 'tier%3Ag5..g1+solved%3A200..&page='
num = []

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info('start')

    # choice = get_problem_url()
    # send_to_slack(choice)
    # send_email(choice)
    send_message()

    logger.info('finish')


def send_message():
    client = boto3.client('sns',
                          aws_access_key_id=AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                          region_name=AWS_SNS_REGION
                          )

    message = f'오늘의 문제입니다! 문제가 없습니다 ㅋㅋ'
    for pp in PHONENUMBER:
        response = client.publish(PhoneNumber=f'+82{pp}', Message=message)


def send_email(choice):
    SUBJECT = "오늘의 문제입니다 !"
    BODY_TEXT = '-'
    BODY_HTML = f"""<html>
    <head></head>
    <body>
      <h1>오늘의 문제입니다 !</h1>
      <p>
        <a href='https://www.acmicpc.net/problem/{choice[0]}'>{choice[0]}</a>
        <a href='https://www.acmicpc.net/problem/{choice[1]}'>{choice[1]}</a>
      </p>
    </body>
    </html>
                """

    client = boto3.client('ses',
                          aws_access_key_id=AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                          region_name=AWS_REGION)
    try:
        response = client.send_email(
            Destination={
                'ToAddresses': RECIPIENT,
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': 'UTF-8',
                        'Data': BODY_HTML
                    },
                    'Text': {
                        'Charset': 'UTF-8',
                        'Data': BODY_TEXT
                    }
                },
                'Subject': {
                    'Charset': 'UTF-8',
                    'Data': SUBJECT
                }
            },
            Source=SENDER
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print('Email Sent ! Message ID:', response['MessageId'])


def send_to_slack(choice):
    payload = {
        'text': '오늘의 문제입니다.',
        'attachments': [{
            'fields': [{
                'title': '문제 #1',
                'value': f'https://www.acmicpc.net/problem/{choice[0]}'
            },
                {
                    'title': '문제 #2',
                    'value': f'https://www.acmicpc.net/problem/{choice[1]}',
                }]
        }]
    }
    requests.post(SLACK_WEBHOOK_URL, data=json.dumps(payload))


def get_problem_url():
    for pp in range(1, 10):
        rr = requests.get(url + str(pp))
        dd = rr.content.decode()
        dd_list = dd.split('<span><a href="https://www.acmicpc.net/problem/')
        if len(dd_list) < 2:
            break
        for ii in range(1, len(dd_list)):
            num.append(dd_list[ii].split('"')[0])

    return random.sample(num, 2)


if __name__ == "__main__":
    lambda_handler(None, None)
