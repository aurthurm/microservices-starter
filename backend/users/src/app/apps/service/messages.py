import os
import requests #httpx

session = requests.Session()
session.trust_env = False


MESSAGES_SERVICE_API_URL = 'http://messages:8051/messages/api/v1/'
MESSAGES_SERVICE_GQL_URL = 'http://localhost/messages/graphql'

def messages_mail_processor(payload):
    url = os.environ.get('MESSAGES_SERVICE_API_URL') or MESSAGES_SERVICE_API_URL
    # r = requests.post(f"{url}mail-processor", data=payload)
    r = session.post(f"{url}mail/mail-processor", json=payload)
    print(r.status_code)
    print(r.text)    
    if r.status_code == 200:
        return {"message": "Success", "detail": f"{r.text}", "status": f"{r.status_code}"}
    else:
        return {"message": "Errored out", "detail": f"{r.text}", "status": f"{r.status_code}"}