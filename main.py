import codecs
import requests
import datetime
import pandas as pd
import logging
from keboola import docker
from mailgun_fun.mailgun import send_complex_message

logging.info('Packages imported succesfully')

### Setting up the docker environment
cfg = docker.Config('/data/')
mailing_list_name = cfg.get_parameters()['mailing_list_name']
USER = cfg.get_parameters()['USER']
PASSWORD = cfg.get_parameters()['#token']
from_id = cfg.get_parameters()['from_id']
subject = cfg.get_parameters()['subject']
html_name = cfg.get_parameters()['html_body']
url = cfg.get_parameters()['url']

try:
    delivery_time = cfg.get_parameters()['delivery_time']
except:
    delivery_time = datetime.datetime.utcnow().strftime('%H:%M:%S')\
                    + ' +0000'

try:
    att = cfg.get_parameters()['attachments']
except:
    att = None

logging.info('Parameters fetched successfully')

scheduled_delivery_date = datetime.datetime.\
                            today().strftime('%a, %d %b %Y ') + delivery_time


path_html = '/data/in/files/' + html_name
html_file = codecs.open(path_html, 'r').read()


mailing_list_path = '/data/in/tables/' + mailing_list_name
mailing_list = pd.read_csv(filepath_or_buffer=mailing_list_path)

logging.info('All done. Ready for mailgun.')

for index, row in mailing_list.iterrows():
    html_body = html_file % row
    to_id = '%(name)s <%(email)s>' % row

    send_status = send_complex_message(to_id,
                                       from_id, 
                                       subject,
                                       html_body,
                                       url,
                                       USER,
                                       PASSWORD,
                                       scheduled_delivery_date,
                                       attachments=att)

    if send_status.ok:
        print('Mail to %(email)s has been sent' % row)
