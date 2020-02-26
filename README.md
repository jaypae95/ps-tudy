# ps-tudy

- 구성원 세 명이 모두 풀지 않는 문제 중 특정 조건에 맞게 필터링
  - ex) 세 명이 모두 풀지 않았으며, 난이도는 실버1 ~ 골드3 사이, 문제 푼 사람 수는 200명 이상 필터
- 두 문제 씩 뽑아 Slack webhook 메시지로 전송

## aws lambda
- 정해진 시간, 월요일 ~ 금요일 오후 8시에 두 문제씩 뽑기 위해 aws의 lambda 이용

1. lambda.py에서 username들과 slack_webhook_url 정보 입력 (필터도 원하는대로)
1. 해당 repository 전체를 다음과 같은 구조가 되도록 압축
```
xxxx.zip _
         |_ bin
         |_certifi
         |_ ...
         |_ ...
         |_ lambda.py
         |_ README.md
```
(lambda.py와 README.md를 제외한 나머지 파일들은 `pip3 install requests .`를 통해 생성)

- aws lambda 생성
    1. aws 로그인
    1. https://ap-northeast-2.console.aws.amazon.com/lambda 접속
    1. Create function 클릭
    1. Function name을 원하는대로 입력 후 Runtime은 python3.7로 설정
    1. Create function 클릭 
    1. Function code에서 Code entry type을 Upload a .zip file로 변경
    1. 압축한 zip파일을 업로드
    1. Handler를 lambda.lambda_hanlder로 수정 ( filename.handler-method )
    1. 위에 Add trigger를 클릭하여 Cloudwatch Events 클릭
    1. Create a new rule 클릭
    1. Rule name 작성
        - ex)mon-fri-8pm-kst
    1. Schedule expression에서 cron(00 11 ? * MON-FRI *) (예시, UTC기준이라 원하는 시간 -9) 입력
        - http://docs.aws.amazon.com/lambda/latest/dg/tutorial-scheduled-events-schedule-expressions.html
    1. Add 클릭
