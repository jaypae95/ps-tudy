import requests
import json
import random
import logging

username1 = ''
username2 = ''
username3 = ''

slack_webhook_url = ''
url = 'https://solved.ac/search?query=-solved_by%3A{0}%20-solved_by%3A{1}%20-solved_by%3A{2}%20tier%3As2..s1%20solved%3A200..?page='.format(username1, username2, username3)

num = []

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info('start')

    main_event()

    logger.info('finish')


def main_event():
    for pp in range(1, 10):
        rr = requests.get(url + str(pp))
        dd = rr.content.decode()
        dd_list = dd.split('<td><a class="problem_id " href="//acmicpc.net/problem/')
        if len(dd_list) < 2:
            break
        for ii in range(1, len(dd_list)):
            num.append(dd_list[ii].split('"')[0])

    choice = random.sample(num, 2)
    print('https://www.acmicpc.net/problem/%s' % choice[0])
    print('https://www.acmicpc.net/problem/%s' % choice[1])

    payload = {
        'text': '오늘의 문제입니다.',
        'attachments': [{
            'fields': [{
                'title': '문제 #1',
                'value': 'https://www.acmicpc.net/problem/%s' % choice[0],
            },
                {
                    'title': '문제 #2',
                    'value': 'https://www.acmicpc.net/problem/%s' % choice[1],
                }]
        }]
    }
    requests.post(slack_webhook_url, data=json.dumps(payload))


if __name__ == "__main__":
    lambda_handler(None, None)
