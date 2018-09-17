import requests



def send_complex_message(to_id, 
                        from_id, 
                        subject, 
                        html_body,
                        delivery_date="Mon, 01 Jan 2018 09:00:00 -0000", 
                        attachments=None):
    '''
    to, from_id, subject, and html_body should be self explanatory.
    attachments is a list of file paths, like this:

    ['/tmp/tmp5paoks/image001.png','/tmp/tmp5paoks/test.txt']
    '''


    data={"from": from_id,
          "to": [to_id, ""],
          "subject": subject,
          "html": html_body,
          "o:deliverytime": delivery_date}

    files = None      
    if attachments:
        files = {}
        count = 0
        for attachment in attachments:
            with open(attachment, 'rb') as f:
                files['attachment['+str(count)+']'] = (os.path.basename(attachment), f.read())    
            count = count + 1

    return requests.post(live_url, 
        auth=(USER, PASSWORD),
        files=files,
        data=data)