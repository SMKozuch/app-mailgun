"__author__ = 'Samuel Kozuch'"
"__credits__ = 'Keboola 2018'"
"__project__ = 'ex-looker'"

"""
Python 3 environment 
"""

import sys
import os
import logging
import json
import codecs
import pandas as pd
import datetime
import requests
import re
import logging_gelf.handlers
import logging_gelf.formatters
from keboola import docker
from mailgun.mailgun import send_complex_message
from mailgun.delivery_check import delivery_time_check



### Environment setup
abspath = os.path.abspath(__file__)
script_path = os.path.dirname(abspath)
os.chdir(script_path)
sys.tracebacklimit = 0

### Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)-8s : [line:%(lineno)3s] %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S")

logger = logging.getLogger()
logging_gelf_handler = logging_gelf.handlers.GELFTCPSocketHandler(
    host=os.getenv('KBC_LOGGER_ADDR'),
    port=int(os.getenv('KBC_LOGGER_PORT'))
    )
logging_gelf_handler.setFormatter(logging_gelf.formatters.GELFFormatter(null_character=True))
logger.addHandler(logging_gelf_handler)

# removes the initial stdout logging
logger.removeHandler(logger.handlers[0])

### Access the supplied rules
cfg = docker.Config('/data/')
params = cfg.get_parameters()
user = params['user']
password = params['#password']
from_name = params['from_name']
domain = params['domain']

logging.info("Successfully fetched all parameters.")

### Tables congig
cfg = docker.Config('/data/')
in_tables = cfg.get_input_tables()
out_tables = cfg.get_expected_output_tables()
logging.info("IN tables mapped: "+str(in_tables))
logging.info("OUT tables mapped: "+str(out_tables))

### Files config
in_files = cfg.get_input_files()
logging.info("IN files mapped: "+str(in_files))
DEFAULT_FILE_INPUT = '/data/in/files/'

### Won't accept more than 1 input table with specified columns
if len(in_tables) > 1:
    logging.error("Please use only one table as input table.")
    sys.exit(1)
elif len(in_tables) == 0:
    logging.error("No input table was inputted. Please specify a table.")
    sys.exit(1)
else:
    pass


def attachment_check(attachment_string, silent=False):
    """
    Function to check attachments
    """
    if len(attachment_string) == 0:
        if silent:
            pass
        else:
            return None

    attachments = [att.strip() for att in attachment_string.split(',')]

    for att in attachments:
        if att == '':
            attachments.remove(att)
        elif att not in os.listdir(DEFAULT_FILE_INPUT) and att != '':
            msg1 = "File %s is not in the directory." % att
            msg2 = "List of available files is: %s" % os.listdir(DEFAULT_FILE_INPUT)
            logging.error(" ".join([msg1, msg2]))
            sys.exit(1)

    if silent:
        pass
    else:
        return attachments

def html_check(file):
    """
    Dummy function that checks, whether html file is in dir.
    """

    if file not in os.listdir(DEFAULT_FILE_INPUT):
        msg1 = "File %s is not in the directory." % file
        msg2 = "List of available files is: %s" % os.listdir(DEFAULT_FILE_INPUT)
        logging.error(" ".join([msg1, msg2]))
        sys.exit(1)
    else:
        try:
            codecs.open('/data/in/files/' + file, 'r').read()
            logging.info("File %s read successfully" % file)
        except:
            logging.error("Could not read file %s." % file)
            sys.exit(2)

def main():
    ### Making sure all columns are included
    mailing_list = pd.read_csv(in_tables[0]['full_path']).fillna("")
    col_spec = set(["email", "name", "html_file", "subject", "attachments", "delivery"])
    col_boolean = len(col_spec.difference(set(list(mailing_list)))) != 0

    if col_boolean:
        msg1 = "Input table does not contain all the necessary columns."
        msg2 = "Missing columns are: %s." % str(col_spec.difference(set(list(mailing_list))))
        msg3 = "Please see documentation for more information."
        logging.error(" ".join([msg1, msg2, msg3]))
        sys.exit(1)
    
    ### Mailgun variables
    from_id = from_name + ' <postmaster@%s>' % domain
    domain_url = 'https://api.mailgun.net/v3/%s/messages' % domain
    
    ### ANTI-SPAM 
    ### if any of the attachments or html bodies is not present
    ### an error will be thrown. This is done before any email
    ### is sent, so that if somebody tries to run the application
    ### again, the person in mailing list won't be spammed.
    for _, row in mailing_list.iterrows():
        html = row['html_file']
        att = row['attachments']
        logging.info("Checking html file %s." % html)
        html_check(html)
        logging.info("Checking attachments %s." % att)
        attachment_check(att)
        logging.info("Attachments checked.")

    for _, row in mailing_list.iterrows():
        ### Recipient variables
        to_id = '%(name)s <%(email)s>' % row
        html_path = DEFAULT_FILE_INPUT + row['html_file']
        html_body = codecs.open(html_path, 'r').read() % row
        delivery = delivery_time_check(row['delivery'])
        attachments = attachment_check(row['attachments'])

        logging.debug("Sending message to %(email)s." % row)

        ### Sending a message
        msg = send_complex_message(to_id,
                                    from_id,
                                    row['subject'],
                                    html_body,
                                    domain_url,
                                    user,
                                    password,
                                    delivery,
                                    attachments)

        if msg.status_code == 200:
            logging.info("An email to %(email)s was sent successfully." % row)
        elif msg.status_code == 401:
            msg1 = "Logging in to Mailgun failed."
            msg2 = "Attempt failed with %s %s" % (msg.status_code, msg.reason)
            logging.error(" ".split([msg1, msg2]))
            sys.exit(1)
        else:
            msg1 = "Could not send a message. Process exited"
            msg2 = "with %s %s" % (msg.status_code, msg.reason)

if __name__=='__main__':
    main()

    logging.info("Script finished.")