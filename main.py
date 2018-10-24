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



### Environment setup
abspath = os.path.abspath(__file__)
script_path = os.path.dirname(abspath)
os.chdir(script_path)
sys.tracebacklimit = 0

### Logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)-8s : [line:%(lineno)3s] %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S")

"""
logger = logging.getLogger()
logging_gelf_handler = logging_gelf.handlers.GELFTCPSocketHandler(
    host=os.getenv('KBC_LOGGER_ADDR'),
    port=int(os.getenv('KBC_LOGGER_PORT'))
    )
logging_gelf_handler.setFormatter(logging_gelf.formatters.GELFFormatter(null_character=True))
logger.addHandler(logging_gelf_handler)

# removes the initial stdout logging
logger.removeHandler(logger.handlers[0])
"""


### Access the supplied rules
cfg = docker.Config('/data/')
params = cfg.get_parameters()
user = params['user']
password = params['#password']
from_name = params['from_name']
domain = params['domain']
delivery_time = params['scheduled_delivery']
attachments = params['attachments']

if re.fullmatch(r'([0|1][0-9]|[2][0-3]):[0-5][0-9]:[0-5][0-9] (\+|\-)([0|1][0-9]{3})', 
    delivery_time):
    scheduled_delivery = datetime.datetime\
                            .today().strftime('%a, %d %b %Y ')\
                             + delivery_time
    logging.info("Delivery scheduled for %s" % scheduled_delivery)
else:
    scheduled_delivery = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S') + ' +0000'
    msg1 = "Delivery time was inputted wrong. %s is unsupported." % delivery_time
    msg2 = "Message will be delivered on %s" % scheduled_delivery
    logging.warn(" ".join([msg1, msg2]))



logging.debug("Parameters are: " + str(params))
logging.info("Successfully fetched all parameters.")

### Tables congig
cfg = docker.Config('/data/')
in_tables = cfg.get_input_tables()
out_tables = cfg.get_expected_output_tables()
logging.info("IN tables mapped: "+str(in_tables))
logging.info("OUT tables mapped: "+str(out_tables))