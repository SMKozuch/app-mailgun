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

logging.info("Successfully fetched all parameters.")