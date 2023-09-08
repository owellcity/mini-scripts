# Python 3.7.3
import requests
import json
import time

# Downloads payslips from bridgepay

# Creates Login Session
session = requests.Session()
url_login = "https://opswerks.bridgepayday.ph/api/auth/login"
creds = '{"username": "CHANGEME", "password": "CHANGEME"}' # > CHANGE USER AND PASSWORD
payload_creds = json.loads(creds)
headers = {'Accept':'application/json, text/plain, */*',
         'Accept-Encoding': 'gzip, deflate, br',
         'Accept-Language': 'en-US,en;q=0.5',
         'Content-Length': '45',
         'Content-Type': 'application/json'}

print("Opening session to {}".format(url_login))
login_session = session.post(url=url_login, json=payload_creds, headers=headers)
time.sleep(3)

# Appending Authentication Bearer token to headers, used for session get requests
headers['Authorization'] = "Bearer {}".format(login_session.json()['token'])

# Getting Employee info
print("Getting employee info..")
url_employees = "https://opswerks.bridgepayday.ph/api/employees"
employee_info = session.get(url=url_employees, headers=headers)
employee_id = employee_info.json()[0]["employeeId"]
time.sleep(6)

# Getting list of payrolls
print("Getting list of payrolls..")
while True:
    url_payslips = "https://opswerks.bridgepayday.ph/api/view-models/payslips-list?$filter=employeeId%20eq%20{}&$orderby=dateEnd%20desc".format(employee_id)
    payslips_info = session.get(url=url_payslips, headers=headers)
    if payslips_info.status_code == 200:
        break
    time.sleep(3)
    print("Retrying: {}".format(url_payslips)) # for somereason, it needs to retry atleast once

# Download payslips
print("Downloading payslips..")
url_payslip = "https://opswerks.bridgepayday.ph/api/ssrs-reports/download"

for payslip in payslips_info.json():
    payload_request = {"reportType":"OPSWERKS/Reports/Payslip","parameters":"&payroll_id={}&employee_id={}".format(payslip['payrollId'], employee_id),"exportType":"PDF","filename":"","password":"","employeeId":employee_id}
    payload_request = json.loads(json.dumps(payload_request))

    payslip_session = session.post(url=url_payslip, json=payload_request, headers=headers)
    if payslip_session.status_code == 200:
        filename = payslip['payrollCode'] + ".pdf"
        with open(filename, "wb") as f:
            for chunk in payslip_session.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print("{}\tDownloaded..".format(filename))
