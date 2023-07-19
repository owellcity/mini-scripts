import requests
import json

# Creates Login Session
session = requests.Session()
url_login = "https://opswerks.bridgepayday.ph/api/auth/login"
payload_creds = json.loads('{"username": "", "password": ""}')
headers = {'Accept':'application/json, text/plain, */*',
         'Accept-Encoding': 'gzip, deflate, br',
         'Accept-Language': 'en-US,en;q=0.5',
         'Content-Length': '45',
         'Content-Type': 'application/json'}

print("Opening session to {}".format(url_login))
login_session = session.post(url=url_login, json=payload_creds, headers=headers)

# Download payslips
print("Downloading payslips..")
url_payslip = "https://opswerks.bridgepayday.ph/api/ssrs-reports/download"
payroll_id = 1
while payroll_id < 32:
    # todo, make payload_request dynamic to anyone
    payload_request = {"reportType":"OPSWERKS/Reports/Payslip","parameters":"&payroll_id=1&employee_id=xx","exportType":"PDF","filename":"Ramos, Guiller Calmerin","password":"","employeeId":xx}
    payload_request["parameters"] = "&payroll_id={}&employee_id=xx".format(payroll_id)
    payload_request = json.loads(json.dumps(payload_request))

    headers = {'Accept':'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
            'Authorization': 'Bearer {}'.format(login_session.json()['token']),
            'Content-Type': 'application/json'}

    payslip_session = session.post(url=url_payslip, json=payload_request, headers=headers)
    # Captures data stream and compiles it
    if payslip_session.status_code == 200:
        filename = "payroll_{}.pdf".format(payroll_id)
        with open(filename, "wb") as f:
            for chunk in payslip_session.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print("{}\tDownloaded..".format(filename))

    payroll_id += 1
