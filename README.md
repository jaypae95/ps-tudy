# ps-tudy

- 구성원 세 명이 모두 풀지 않는 문제 중 특정 조건에 맞게 필터링
  - ex) 세 명이 모두 풀지 않았으며, 난이도는 실버1 ~ 골드3 사이, 문제 푼 사람 수는 200명 이상 필터
- 두 문제 씩 뽑아 Slack webhook 메시지로 전송

## settings
- `cp settings_local_sample.py settings_local.py` 내용 기입
- 공통
  - 구성원 백준 아이디 USERNAME
- slack 사용 시 
  - SLACK_WEBHOOK_URL
- ses 사용 시
  - SENDER
  - AWS_REGION
  - AWS_ACCESS_KEY_ID
  - AWS_SECRET_ACCESS_KEY

## aws lambda
- 정해진 시간, 월요일 ~ 금요일 오후 8시에 두 문제씩 뽑기 위해 aws의 lambda 이용

1. lambda.py에서 username들과 slack_webhook_url 정보 입력 (필터도 원하는대로)
2. 해당 repository 전체를 다음과 같은 구조가 되도록 압축
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

3. aws lambda 생성
    1. aws 로그인
    2. https://ap-northeast-2.console.aws.amazon.com/lambda 접속
    3. Create function 클릭
    4. Function name을 원하는대로 입력 후 Runtime은 python3.7로 설정
    5. Create function 클릭 
    6. Function code에서 Code entry type을 Upload a .zip file로 변경
    7. 압축한 zip파일을 업로드
    8. Handler를 lambda.lambda_hanlder로 수정 ( filename.handler-method )
    9. 위에 Add trigger를 클릭하여 Cloudwatch Events 클릭
    10. Create a new rule 클릭
    11. Rule name 작성
         - ex)mon-fri-8pm-kst
    12. Schedule expression에서 cron(00 11 ? * MON-FRI *) (예시, UTC기준이라 원하는 시간 -9) 입력
         - http://docs.aws.amazon.com/lambda/latest/dg/tutorial-scheduled-events-schedule-expressions.html
    13. Add 클릭

## aws ses
   1. access key 발급 후 settings_local에 작성
   2. aws ses에서 email verfiy