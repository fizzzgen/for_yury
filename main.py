import time
import pickle
import os.path
import pprint

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import validate_email

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import _config

email_group_counter = 0


def send_email(
        to_addr,
        subject=_config.EMAIL_SUBJECT,
        text='please add real text',
        img_path=_config.IMG_PATH,
        login=_config.MAIL_LOGIN,
        password=_config.MAIL_PASS,
        server=_config.SERVER,
        retry_nums=_config.RETRY_NUM,
        retry_interval=_config.RETRY_INTERVAL,
):
    global email_group_counter

    # Retrying to send message if not success
    for i in range(retry_nums):
        email_group_counter += 1
        try:
            server = smtplib.SMTP_SSL(server)
            server.login(login, password)
            server.auth_plain()
            message = "\r\n".join([
                "From: {}".format(login),
                "To: {}".format(to_addr),
                "Subject: {}".format(subject),
                "",
                text
            ])
            server.sendmail(login, to_addr, message.encode('utf-8'))
            server.quit()
            print('SUCCESS: message to {} sent'.format(to_addr))
            return True
        except Exception as ex:
            print('FAIL: message to {} not sent: {}'.format(to_addr, repr(ex)))
            time.sleep(retry_interval)
    time.sleep(_config.SEND_INTERVAL)
    if email_group_counter > _config.EMAILS_IN_GROUP:
        time.sleep(_config.GROUP_SEND_INTERVAL)
        email_group_counter = 0
    else:
        time.sleep(_config.SEND_INTERVAL)
    return False


def parse_google_table():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', _config.SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=_config.SAMPLE_SPREADSHEET_ID,
                                range=_config.SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])
    validated_values = []
    if not values:
        print('No data found.')
    else:
        with open('invalid_rows.txt', 'w') as f:
            for row in values:
                if len(row) < 4:
                    f.write(str(row) + '\n')
                    print('SPREADSHEET ROW {} SKIPPED: NO ADDRESS'.format(row))
                    continue
                validated_values.append(row)
    return [{'email': row[0], 'name': row[1], 'address': row[3]} for row in validated_values]


def configure_pairs():
    pairs = []
    emails = parse_google_table()

    with open('invalid_emails.txt', 'w') as f:
        for email in emails:
            if not validate_email.validate_email(email['email'], verify=True) or email['address'] is None:
                print("INVALID EMAIL DETECTED AND DELETED: {}".format(email['email']))
                f.write(email['email'])
                emails.remove(email)

    assert len(emails) >= 1

    for i in range(1, len(emails)):
        pairs.append({'sender': emails[i - 1], 'receiver': emails[i]})
    pairs.append({'sender': emails[len(emails) - 1], 'receiver': emails[0]})
    with open('calculated_pairs.txt', 'w') as f:
        f.write('Sender, Reseiver\n')
        f.writelines('{}, {}\n'.format(pair['sender']['email'], pair['receiver']['email']) for pair in pairs)
    return pairs


def send_happy_new_year():
    pairs = configure_pairs()
    n = len(pairs)
    for pair in pairs:
        print("Emails left: . . . . . . . . . . . . . . . . . . . . . . . . {}".format(n))
        send_email(
            to_addr=pair['sender']['email'],
            text=_config.EMAIL_TEXT.format(
                sender_name=pair['sender']['name'],
                receiver_name=pair['receiver']['name'],
                receiver_address=pair['receiver']['address']
            )
        )
        n -= 1
    pass


def _test_email():
    send_email('lasercrypto@yandex.ru', 'test_success', 'lol')
    send_email('fizzzgen@gmail.com', 'test_fail', 'lol')
    send_email('lasercrypto@yandex.ru', 'test_success', 'lol')


def _test_parsing():
    pprint.pprint(parse_google_table())


def _test_configure_pairs():
    pprint.pprint(configure_pairs())


def _test_send_happy_new_year():
    send_happy_new_year()

send_happy_new_year()
