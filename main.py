import sys
import codecs
import requests
import datetime
import pandas as pd
import logging
from keboola import docker
from mailgun_fun.mailgun import send_complex_message



sys.tracebacklimit = 0

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s: [%(filename)s:%(funcName)s:line %(lineno)s] %(message)s')
logger = logging.getLogger()
###################################################################################################################

logging.info("Fetching parameters...")
cfg = docker.Config('/data/')

try:
    mailing_list_name = cfg.get_parameters()['mailing_list_name']
except:
    logging.error('The path to mailing list was not specified correctly or file does not exist.')
    sys.exit(1)


USER = cfg.get_parameters()['USER']
PASSWORD = cfg.get_parameters()['#token']

try:
    from_id = cfg.get_parameters()['from_id']
except:
    logging.error("From ID was not specified.")
    sys.exit(1)

try:
    subject = cfg.get_parameters()['subject']
except:
    logging.error('Subject of email message was not specified.')
    sys.exit(1)

try:
    html_name = cfg.get_parameters()['html_body']
except:
    logging.error('HTML body was not specified.')
    sys.exit(1)

try:
    url = cfg.get_parameters()['url']
except:
    logging.error('URL was not specified.')
    sys.exit(1)

try:
    delivery_time = cfg.get_parameters()['delivery_time']
except:
    delivery_time = datetime.datetime.utcnow().strftime('%H:%M:%S')\
                    + ' +0000'

try:
    att = cfg.get_parameters()['attachments']
except:
    att = None

logging.info('Parameters fetched successfully.')

scheduled_delivery_date = datetime.datetime.\
                            today().strftime('%a, %d %b %Y ') + delivery_time

logging.info("Emails will be delivered on %s" % scheduled_delivery_date)


path_html = '/data/in/files/' + html_name

try:
    html_file = codecs.open(path_html, 'r').read()
except:
    logging.error("""HTML file could not be read. Please make sure 
                    that you provided right path to filename in form 
                    ID_name.html, where ID is Keboola Storage ID and 
                    name is the name of the file.""")
    sys.exit(1)


mailing_list_path = '/data/in/tables/' + mailing_list_name

try:
    mailing_list = pd.read_csv(filepath_or_buffer=mailing_list_path)
except:
    logging.error("""Mailing list could not be read. 
                    Please make sure that you inputted the name 
                    of input table correctly.""")
    sys.exit(1)

logging.info('All the files were fetched.')

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
        logging.info('Mail to %(email)s has been sent.' % row)
    else:
        logging.warn("""Mail to %(email)s was not sent. Please 
                        refer to Mailgun dashboard for more information.""" % row)

logging.info("Script finished.")
sys.exit(0)