# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']          # dont't change

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1yJg-8qbG8P8l7oT4kGHvflz6RGW5d4ki1PxcUjDdsvk'      # sheet id
SAMPLE_RANGE_NAME = 'LeadsFromTilda!A2:G100000000'                          # sheet_name!your_range

MAIL_LOGIN = 'new-year@simple-digital.ru'                                   # login for mail
MAIL_PASS = 'qazwsxedc123'                                                  # password for mail

SERVER = 'smtp.yandex.ru:465'                                               # mail smtp server

RETRY_NUM = 2                                                               # number of retries if failing to send message
RETRY_INTERVAL = 3                                                          # interval of retries in seconds

SEND_INTERVAL = 1                                                           # send interval in seconds

GROUP_SEND_INTERVAL = 600                                                   # send interval between groups
EMAILS_IN_GROUP = 100                                                       # number of emails in group

EMAIL_SUBJECT = 'Test subject'

# in text you should use {sender_name},{receiver_name} and {receiver_address}.
# they will be changed for generated values
EMAIL_TEXT = 'Hello, {sender_name}, u need to make a punch for {receiver_name} {receiver_address}'

assert (
        '{sender_name}' in EMAIL_TEXT and
        '{receiver_name}' in EMAIL_TEXT and
        '{receiver_address}' in EMAIL_TEXT
)
IMG_PATH = 'test.png'                                                       # "None" for no img, else path from executing
                                                                            # directory