import requests
from enum import Enum
from datetime import datetime
import json

'''
Loads cookie from file
'''
def load_cookie(cookie_file_path = './cookie.txt'):
    with open(cookie_file_path) as cookie_file:
        return cookie_file.readline()

'''
Define an enum class indicating export status
'''
class Status(Enum):
    FAILED = 1,
    SUCCESS = 0

'''
Send out email notification based on export status
'''
def mail_notification(type):
    pass


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
        mail_notification(Status.FAILED)
    else:
        response = ret.json()
        data_start_date = response['dataStartDate']
        date_end_date = response['dataEndDate']
        save_data_to_local(data_start_date / 1000, date_end_date / 1000, response)
        mail_notification(Status.SUCCESS)
    pass

if __name__ == "__main__":
    cookie = load_cookie()
    export_data_from_solar_edge(cookie)