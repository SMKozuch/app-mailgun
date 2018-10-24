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

logging.debug("Parameters are: " + str(params))
logging.info("Successfully fetched all parameters.")

### Tables congig
cfg = docker.Config('/data/')
in_tables = cfg.get_input_tables()
out_tables = cfg.get_expected_output_tables()
logging.info("IN tables mapped: "+str(in_tables))
logging.info("OUT tables mapped: "+str(out_tables))

if len(in_tables) > 1:
    logging.error("Please use only one table as input table.")
    sys.exit(1)
elif len(in_tables) == 0:
    logging.error("No input table was inputted. Please specify a table.")
    sys.exit(1)
else:
    pass

mailing_list = pd.read_csv(in_tables[0]['full_path'])
col_spec = set(["email", "name", "html_file", "attachments", "delivery"])

col_boolean = col_spec != set(list(mailing_list))

if col_boolean:
    msg1 = "Input table does not contain all the necessary columns."
    msg2 = "Missing columns are: %s." % str(col_spec.difference(set(list(mailing_list))))
    msg3 = "Please see documentation for more information."
    logging.error(" ".join([msg1, msg2, msg3]))
    sys.exit(1)

