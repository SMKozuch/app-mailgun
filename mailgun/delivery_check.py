import datetime
import re
import logging



def delivery_time_check(delivery_time):
    """
    Dummy function that checks, whether delivery time was correctly inputted.
    """

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
    
    return scheduled_delivery