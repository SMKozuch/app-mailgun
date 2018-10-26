import os
import requests



def send_complex_message(to_id, 
                        from_id, 
                        subject, 
                        html_body, 
                        live_url,
                        username,
                        password,
                        delivery_date="Mon, 01 Jan 2018 09:00:00 -0000",
                        attachments=None):
    '''
    to, from_id, subject, and html_body should be self explanatory.
    attachments is a list of file paths, like this:

    ['/tmp/tmp5paoks/image001.png','/tmp/tmp5paoks/test.txt']
    '''

    if delivery_date:
        data={"from": from_id,
            "to": [to_id, ""],
            "subject": subject,
            "html": html_body,
            "o:deliverytime": delivery_date}
    else:
        data={"from": from_id,
            "to": [to_id, ""],
            "subject": subject,
            "html": html_body}

    files = None      
    if attachments:
        files = {}
        count = 0
        for attachment in attachments:
            path = '/data/in/files/' + attachment
            with open(path, 'rb') as f:
                files['attachment['+str(count)+']'] = (os.path.basename(path), f.read())    
            count = count + 1

    return requests.post(live_url, 
        auth=(username, password),
        files=files,
        data=data)