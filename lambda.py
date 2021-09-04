from settings_local import USERNAME
import requests
import json
import random
import logging


slack_webhook_url = ''
url = 'https://solved.ac/search?query='
for uu in range(len(USERNAME)):
    url += f'-solved_by%3A{USERNAME[uu]}+'
url += 'tier%3Ag5..g1+solved%3A200..&page='
num = []

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info('start')

    send_to_slack()

    logger.info('finish')


def send_to_slack():
    for pp in range(1, 10):
        rr = requests.get(url + str(pp))
        dd = rr.content.decode()
        dd_list = dd.split('<span><a href="https://www.acmicpc.net/problem/')
        if len(dd_list) < 2:
            break
        for ii in range(1, len(dd_list)):
            num.append(dd_list[ii].split('"')[0])

    choice = random.sample(num, 2)
    print('https://www.acmicpc.net/problem/%s' % choice[0])
    print('https://www.acmicpc.net/problem/%s' % choice[1])
    print(url)
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
