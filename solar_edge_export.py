import requests
import time
import json
import smtplib
from email.message import EmailMessage

'''
Loads cookie from file
'''
def load_cookie(cookie_file_path = './cookie.txt'):
    with open(cookie_file_path) as cookie_file:
        return cookie_file.readline()

'''
Send out email notification based on export status
'''
def mail_failure_notification():
    gmail('Solar Edge Generation Export Failed!', 'Is cookie expired?')

def gmail(subject, content):
    email_address = 'zhaosheng922@gmail.com'
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login('zhaosheng922', load_email_password())
        msg = EmailMessage()
        msg.set_content(content)
        msg['Subject'] = subject
        msg['From'] = email_address
        msg['To'] = email_address
        smtp.send_message(msg)


def mail_daily_generation_summary(daily_generation):
    gmail('Solar Edge Generation Daily Summary', '%d kwh on %s' % (daily_generation['production'], daily_generation['day']))


def load_email_password(password_file = './password'):
    with open(password_file, 'r') as f:
        return f.read()

'''
Save exported data file to local for historical tracking purpose
'''
def save_data_to_local(start_time, end_time, json_content):
    file_to_save = './data_export/solar_edge_export_%d_%d.json' % (start_time, end_time)
    with open(file_to_save, 'w') as target:
        target.write(json.dumps(json_content, indent=4))    # pretty print Json


def export_data_from_solar_edge(cookie):
    url = 'https://monitoring.solaredge.com/solaredge-apigw/api/site/1040575/powerDashboardChart?chartField=DAY&foldUp=true&activeTab=0&fieldId=1040575&endDate=&perserveTabsData=true'
    headers = {
        'Cookie': cookie
    }
    ret = requests.get(url, headers=headers)
    if ret.status_code != 200:
        # Failed to get response, cookie expired?
        mail_failure_notification()
    else:
        response = ret.json()
        data_start_date = response['dataStartDate'] / 1000
        date_end_date = response['dataEndDate'] / 1000
        save_data_to_local(data_start_date, date_end_date, response)
        data = {
            'production': response['utilizationMeasures']['production']['value'],
            'day': time.strftime('%Y-%m-%d', time.localtime(data_start_date))
        }
        mail_daily_generation_summary(data)

if __name__ == "__main__":
    cookie = load_cookie()
    export_data_from_solar_edge(cookie)